from tortoise import Tortoise
from config import settings


async def register_db():
    await Tortoise.init(settings.DB_CONFIG_DICT)
    await Tortoise.generate_schemas()


async def close_db():
    await Tortoise.close_connections()
