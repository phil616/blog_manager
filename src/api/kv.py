from fastapi import APIRouter, Depends
from pydantic import BaseModel
from core.dependencies import get_global_kv, ThreadSafeStorage

kv_router = APIRouter(prefix="/kv")


class KVStore(BaseModel):
    key: str
    value: str


@kv_router.get("/get/{key}")
async def read_item(key: str, g: ThreadSafeStorage = Depends(get_global_kv)):
    return g.get_value(key)


@kv_router.post("/set")
async def set_item(kv: KVStore, g: ThreadSafeStorage = Depends(get_global_kv)):
    g.set_value(kv.key, kv.value)


@kv_router.get("/all")
async def get_all_items(g: ThreadSafeStorage = Depends(get_global_kv)):
    return g.get_all_values()


@kv_router.get("/remove/{key}")
async def remove_item(key: str, g: ThreadSafeStorage = Depends(get_global_kv)):
    g.delete_value(key)
