from api import blog, file, kv, login, article,share,pgp
from fastapi import APIRouter, Security
from core.security import check_permissions

router = APIRouter(prefix="/api")

router.include_router(blog.blog_router, tags=["blog"], dependencies=[Security(check_permissions)])
router.include_router(file.file_router, tags=["file"], dependencies=[Security(check_permissions)])
router.include_router(kv.kv_router, tags=["kv"], dependencies=[Security(check_permissions)])
router.include_router(article.article_router, tags=["article"], dependencies=[Security(check_permissions)])
router.include_router(share.share_router, tags=["share"])
router.include_router(pgp.pgp_router, tags=["pgp"])
router.include_router(login.login_router)

