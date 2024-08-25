from pydantic import (
    computed_field,
    Field,
)
from pydantic_settings import BaseSettings
from typing_extensions import List, Union
from os import path, walk


class Settings(BaseSettings):
    # ---- Project Basic Config ----
    APP_NAME: str = Field(default="Blog API",env="APP_NAME")
    APP_DESC: str = Field(default="Github Blog Management API",env="APP_DESCRIPTION")
    APP_VER: str = Field(default="0.0.1",env="APP_VERSION")
    # ---- Github Settings -----
    BLOG_BRANCH: str = Field(default="main", env="BLOG_BRANCH", description="")

    # ---- Github Blog Directory ----
    BLOG_FOLDER_PATH: str = Field(default="_posts", env="BLOG_FOLDER_PATH", description="博客文件夹路径")
    GITHUB_TOKEN: str = Field(default="CHANGETHIS", env="GITHUB_TOKEN", description="Github Token")
    BLOG_REPO: str = Field(default="CHANGETHIS", env="BLOG_REPO", description="博客仓库名")

    # ---- SMTP Settings ----
    SMTP_PORT: Union[int, str] = Field(default=587, env="SMTP_PORT", description="SMTP端口")
    SMTP_HOST: Union[str, None] = Field(default=None, env="SMTP_HOST", description="SMTP主机")
    SMTP_USER: Union[str, None] = Field(default=None, env="SMTP_USER", description="SMTP用户名")
    SMTP_PASSWORD: Union[str, None] = Field(default=None, env="SMTP_PASSWORD", description="SMTP密码")
    EMAILS_FROM_EMAIL: Union[str, None] = Field(default=None, env="EMAILS_FROM_EMAIL", description="发件人邮箱")

    # ---- CORS ---- # Cross-Origin Resource Sharing Policy
    CORS_ALLOW_ORIGINS: List = ["*"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: List = ["*"]
    CORS_ALLOW_HEADERS: List = ["*"]

    # ---- Secure ---- # JWT (JSON Web Token)
    JWT_SECRET_KEY: str = Field(default="CHANGETHIS", env="JWT_SECRET_KEY", description="JWT密钥")
    JWT_ALGORITHM: str = Field(default="HS256", env="JWT_ALGORITHM", description="JWT算法")
    JWT_ACCESS_EXPIRE_MINUTES: int = Field(default=60, env="JWT_ACCESS_EXPIRE_MINUTES",
                                           description="JWT访问过期时间（分钟）")
    # ---- Switches ----
    ENABLE_BACKEND_CORS_ORIGINS: bool = Field(default=True)  # enable this if on a remote server
    ENABLE_STATIC_DIR: bool = Field(default=False)  # enable this if you want to serve static files
    MODEL_DIR: str = Field(default="model")

    # ---- SQLite FILE ----
    SQLITE_FILE: str = Field(default="db.sqlite3", env="SQLITE_FILE", description="SQLite文件名")

    # ---- System Login ----
    LOGIN_USERNAME: str = Field(default="admin", env="LOGIN_USERNAME", description="登录用户名")
    LOGIN_PASSWORD: str = Field(default="admin123", env="LOGIN_PASSWORD", description="登录密码")

    @computed_field
    @property
    def DB_CONFIG_DICT(self) -> dict:
        skip_files = ['Basic.py', '__init__.py']  # skip package file and BaseTimestampMixin (Basic.py)
        ret = []
        for _, _, i in walk(path.join(self.MODEL_DIR)):
            models = list(set(i) - set(skip_files))
            for model in models:
                model = model.replace(".py", "")
                model = self.MODEL_DIR + "." + model
                ret.append(model)
            break
        return {
            "connections": {
                "default": {
                    "engine": "tortoise.backends.sqlite",
                    "credentials": {"file_path": path.join("storage", self.SQLITE_FILE)},
                }
            },
            "apps": {
                "events": {"models": ret, "default_connection": "default"}
            },
            "timezone": "Asia/Shanghai",
            "use_tz": True,
        }

    class Config:
        env_file = ".env"  # Path to a file containing environment variables


settings = Settings()  # type: ignore
