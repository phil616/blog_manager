from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from base64 import b64decode
from core.background import export_file_to_email
from core.logger import log
from core.utils import gen_random_string
from lib.github_blog import get_repo_blogs, delete_blog_by_name, get_blog_by_name
from core.dependencies import get_global_kv, ThreadSafeStorage

blog_router = APIRouter(prefix="/blog")


@blog_router.get("/all")
async def get_all_blogs(global_kv: ThreadSafeStorage = Depends(get_global_kv)):
    cached = global_kv.get_value("all_blogs")
    if cached:
        log.info("[Cache Hit] Returning all blogs from cache")
        return cached
    else:
        log.info("[Caching] Fetching all blogs from GitHub")
        all_blogs = get_repo_blogs()
        global_kv.set_value("all_blogs", all_blogs)
        return get_repo_blogs()


@blog_router.get("/delete/{id}")
async def delete_blog(name: str, global_kv: ThreadSafeStorage = Depends(get_global_kv)):
    global_kv.delete_value("all_blogs")  # clear cache
    delete_blog_by_name(name)
    return {"message": f"Blog {name} deleted successfully, current queued, cache cleared"}


@blog_router.get("/export")
async def export_blog(filename: str, email: str, background_task: BackgroundTasks):
    b64blog = get_blog_by_name(filename)
    if not b64blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    content = b64decode(b64blog)
    bg_id = gen_random_string(10)  # generate a unique id for the background task
    background_task.add_task(export_file_to_email,
                             filename=filename,
                             message="Blog Export",
                             content=content.decode("utf-8"),
                             send_to=email,
                             bg_id=bg_id)
    return {"message": f"Blog {filename} export started, check your email for the export file", "bg_id": bg_id}
