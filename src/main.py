
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from core.lifespan import app_lifespan
from config import settings
from core.endpoint import router
app = FastAPI(
    description=settings.APP_DESC,
    version=settings.APP_VER,
    title=settings.APP_NAME,
    lifespan=app_lifespan,
)

# Set all CORS enabled origins
if settings.ENABLE_BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ALLOW_ORIGINS,
        allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
        allow_methods=settings.CORS_ALLOW_METHODS,
        allow_headers=settings.CORS_ALLOW_HEADERS,
    )

app.include_router(router)
