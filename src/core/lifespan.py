from fastapi import FastAPI
import contextlib
from core.logger import log
from .db import register_db, close_db


@contextlib.asynccontextmanager
async def app_lifespan(app: FastAPI):
    await register_db()
    log.info("Starting Up lifespan")
    yield
    log.info("Shutting Down lifespan")
    await close_db()
