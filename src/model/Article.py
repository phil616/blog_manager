from typing import List, Union, Optional

from tortoise import Model, fields
from pydantic import BaseModel


class Article(Model):
    id = fields.IntField(pk=True)

    title = fields.CharField(max_length=255)
    tags = fields.CharField(max_length=255, null=True)
    content = fields.TextField()
    decrypted = fields.BooleanField(default=False)

    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "article"


class ArticleSchema(BaseModel):
    title: str
    tags: Optional[str] = None
    content: Union[str, bytes]
    decrypted: Optional[bool] = False


class ArticleResponseSchema(BaseModel):
    id: int
    title: str
    tags: Optional[str] = None
    decrypted: bool

