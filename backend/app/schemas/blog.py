from typing import Optional, List
from pydantic import BaseModel

class BlogPostBase(BaseModel):
    title: str
    content: str
    summary: Optional[str] = None
    keywords: Optional[List[str]] = None
    image_url: Optional[str] = None
    status: Optional[str] = "draft"
    wordpress_post_id: Optional[int] = None

class BlogPostCreate(BlogPostBase):
    pass

class BlogPostUpdate(BlogPostBase):
    title: Optional[str] = None
    content: Optional[str] = None

class BlogPostInDBBase(BlogPostBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True

class BlogPostResponse(BlogPostInDBBase):
    pass
