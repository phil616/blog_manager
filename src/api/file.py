import os

from fastapi import APIRouter, UploadFile, HTTPException
from fastapi.responses import FileResponse

from core.logger import log
from model.File import File
from model.Share import Share
from core.utils import gen_random_string
from aiofiles import open
from os import path, remove
import zipfile

file_router = APIRouter(prefix="/file")


async def write_file(filename: str, content: bytes):
    filepath = path.join("storage", filename)
    async with open(filepath, 'wb') as f:  # 注意这里使用的是 async with
        await f.write(content)


async def read_file(filename: str) -> bytes:
    filepath = path.join("storage", filename)
    async with open(filepath, 'rb') as f:  # 注意这里使用的是 async with
        content = await f.read()
    return content


@file_router.post("/upload", include_in_schema=False)
async def upload_file(file: UploadFile):
    data = await file.read()
    mime = file.content_type
    filename = file.filename
    fid = gen_random_string(32)
    fdb = await File.create(
        fid=fid,
        filename=filename,
        mime=mime,
    )
    await fdb.save()
    await write_file(fid, data)
    return {"fid": file.fid}

@file_router.get("/download/{fid}")
async def download_file(fid: str):
    file = await File.filter(fid=fid).first()
    return FileResponse(path=path.join("storage", file.fid),
                        media_type=file.mimetype,
                        filename=file.filename)


@file_router.get("/list")
async def list_file():
    all_file = await File.all()
    return all_file


@file_router.delete("/delete/{fid}")
async def delete_file(fid: str):
    await File.filter(fid=fid).delete()
    filepath = path.join("storage", fid)
    if path.exists(filepath):
        remove(filepath)
    return {"message": "File deleted successfully"}


@file_router.get("/migrate")
async def migrate_file():
    folder_path = "storage"
    zipfile_id = gen_random_string(32).upper()
    with zipfile.ZipFile(path.join(folder_path, f"{zipfile_id}.zip"), 'w') as zip_file:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = path.join(root, file)
                zip_file.write(file_path, os.path.relpath(file_path, folder_path))

    return FileResponse(path=path.join(folder_path, f"{zipfile_id}.zip"),
                        filename=f"{zipfile_id}.zip",
                        media_type="application/zip")


@file_router.get("/create_share")
async def share_file(fid: str, exp: int = 30):
    ec = gen_random_string(8)
    file = await File.filter(fid=fid).first()
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    await Share.create(
        share_file_id=file.fid,
        filename=file.filename,
        extract_code=ec,
        expire_minutes=exp,
    )
    return {"expire_minutes": exp, "extract_code": ec}
