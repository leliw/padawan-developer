"""Knowledge base article models"""

from datetime import datetime as Datetime
from typing import List, Optional
from pydantic import BaseModel


class ArticleHeader(BaseModel):
    """Knowledge base article header model"""

    title: str
    tags: List[str] = []
    created_at: Optional[Datetime] = None
    updated_at: Optional[Datetime] = None


class Article(ArticleHeader):
    """Knowledge base article model"""

    content: str
