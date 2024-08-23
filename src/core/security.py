from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import Depends, HTTPException, status, Request
from datetime import datetime, timedelta
import jwt
from config import settings as config
from core.logger import log
security = HTTPBasic()


def create_access_token(data: dict):
    token_data = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=config.JWT_ACCESS_EXPIRE_MINUTES)  # JWT过期分钟 = 当前时间 + 过期时间
    token_data.update(
        {
            "exp": expire,
            "iss": config.APP_NAME,
        }
    )
    jwt_token = jwt.encode(
        payload=token_data,  # 编码负载
        key=config.JWT_SECRET_KEY,  # 密钥
        algorithm=config.JWT_ALGORITHM  # 默认算法
    )
    return jwt_token


def check_permissions(req: Request):
    token = None
    try:

        token = req.headers.get("Authorization").split(" ")[1]
        log.debug(f"Token: {token}")
        if not token:
            raise HTTPException(401)

        payload = jwt.decode(token, config.JWT_SECRET_KEY, algorithms=[config.JWT_ALGORITHM])
        usr = payload.get("sub")
        log.debug(f"User: {usr}")

    except Exception as e:
        log.error(f"Certification parse failed: {e}")
        HTTPException(401, detail="Certification parse failed", headers={"WWW-Authenticate": f"Bearer {token}"})
