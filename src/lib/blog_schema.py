from typing import List, Optional

from pydantic import BaseModel
from core.utils import get_current_time


class BlogSchema(BaseModel):
    filename: str
    title: str
    categories: List[str]
    tags: List[str]
    date: str
    b64_content: str

