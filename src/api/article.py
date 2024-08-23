from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks

from core.utils import gen_random_string
from model.Article import Article, ArticleSchema, ArticleResponseSchema
from core.dependencies import get_global_kv, ThreadSafeStorage
from core.logger import log
from config import settings
from lib.aioemail import send_email, Attachment

article_router = APIRouter(prefix="/article")


@article_router.get("/all")
async def get_all_articles(global_kv: ThreadSafeStorage = Depends(get_global_kv)):
    cache = global_kv.get_value("all_articles")
    if cache:
        log.info("[Cache Hit] Returning articles from cache")
        return cache
    all_articles = await Article.all()
    all_articles_schema = []
    for article in all_articles:
        article_schema = ArticleResponseSchema(**article.__dict__)
        all_articles_schema.append(article_schema)
    global_kv.set_value("all_articles", all_articles_schema)
    return all_articles_schema


@article_router.get("/get/{id}")
async def get_article_by_id(id: int):
    article = await Article.filter(id=id).first()
    if article:
        return article.__dict__
    else:
        raise HTTPException(status_code=404, detail="Article not found")


@article_router.post("/create")
async def create_article(article: ArticleSchema, global_kv: ThreadSafeStorage = Depends(get_global_kv)):
    global_kv.delete_value("all_articles")  # delete cache
    await Article.create(**article.model_dump())


@article_router.put("/update/{id}")
async def update_article(id: int, article: ArticleSchema, global_kv: ThreadSafeStorage = Depends(get_global_kv)):
    global_kv.delete_value("all_articles")  # delete cache
    article_db = await Article.filter(id=id).first()
    if article_db:
        await article_db.update_from_dict(article.model_dump())
        await article_db.save()
    else:
        raise HTTPException(status_code=404, detail="Article not found")


@article_router.delete("/delete/{id}")
async def delete_article(id: int, global_kv: ThreadSafeStorage = Depends(get_global_kv)):
    global_kv.delete_value("all_articles")  # delete cache
    article_db = await Article.filter(id=id).first()
    if article_db:
        await article_db.delete()
    else:
        raise HTTPException(status_code=404, detail="Article not found")


@article_router.get("/migrate")
async def migrate_article(email: str,
                          id: int,
                          background_task: BackgroundTasks,
                          global_kv: ThreadSafeStorage = Depends(get_global_kv)
                          ):
    article = await Article.filter(id=id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    bg_id = gen_random_string(10)
    log.info(f"Background task: {bg_id}")

    async def migrate_article_to_email(filename: str, content: str, send_to: str):
        try:
            global_kv.set_value("bg_task_" + bg_id, "running")
            await send_email(
                settings.SMTP_HOST,
                int(settings.SMTP_PORT),
                settings.SMTP_USER,
                settings.SMTP_PASSWORD,
                subject=f"Migrate article {filename}",
                send_to_addr=send_to,
                contest_msg="Migrate article content to email, please check the attachment.",
                text='plain',
                attachments=[Attachment(filename=filename, content=content.encode('utf-8'))]
            )
            global_kv.set_value("bg_task_" + bg_id, "done")
        except Exception as e:
            global_kv.set_value("bg_task_" + bg_id, "error")
            log.error(f"Error while sending email: {e}", exc_info=True)

    background_task.add_task(migrate_article_to_email, filename=article.title + ".md", content=article.content,
                             send_to=email)
    return {"message": "Email sent successfully", "bg_id": bg_id}
