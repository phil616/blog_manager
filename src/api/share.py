from os import path
from core.logger import log
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from model.Share import Share
from model.File import File
from datetime import datetime, timedelta

share_router = APIRouter(prefix="/share")


@share_router.get("/exact")
async def get_share_file_by_exact(exact_code: str):
    log.debug(f"Getting share file by exact code: {exact_code}")
    share_file = await Share.filter(extract_code=exact_code).first()
    if not share_file:
        raise HTTPException(status_code=404, detail="Share file not found")

    create_date = share_file.created_at.replace(tzinfo=None).timestamp()  # datetime object, need to adjust time zone

    expire_minutes = share_file.expire_minutes
    expire_timedelta = create_date + 60 * expire_minutes

    if datetime.now().timestamp() > expire_timedelta:
        raise HTTPException(status_code=404, detail="Share file expired")

    file = await File.filter(fid=share_file.share_file_id).first()
    return FileResponse(path=path.join("storage", file.fid),
                        filename=file.filename,
                        media_type=file.mimetype)
