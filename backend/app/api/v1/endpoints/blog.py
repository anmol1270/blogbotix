from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.auth import get_current_active_user
from app.db.base import get_db
from app.models.user import User
from app.schemas.blog import BlogPostResponse, BlogPostCreate, BlogPostUpdate
from app.services.blog import BlogService

router = APIRouter()

@router.get("/", response_model=List[BlogPostResponse])
async def get_posts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """Get all posts for the current user"""
    posts = BlogService.get_user_posts(db, current_user.id)
    return posts

@router.get("/{post_id}", response_model=BlogPostResponse)
async def get_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """Get a specific post"""
    post = BlogService.get_post(db, post_id, current_user.id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@router.post("/", response_model=BlogPostResponse)
async def create_post(
    *,
    db: Session = Depends(get_db),
    post_in: BlogPostCreate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """Create a new post"""
    post = await BlogService.create_post(db, post_in, current_user.id)
    return post

@router.put("/{post_id}", response_model=BlogPostResponse)
async def update_post(
    *,
    db: Session = Depends(get_db),
    post_id: int,
    post_in: BlogPostUpdate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """Update a post"""
    post = await BlogService.update_post(db, post_id, post_in, current_user.id)
    return post

@router.post("/{post_id}/publish", response_model=BlogPostResponse)
async def publish_post(
    *,
    db: Session = Depends(get_db),
    post_id: int,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """Publish a post to WordPress"""
    try:
        post = await BlogService.publish_post(db, post_id, current_user.id)
        return post
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{post_id}")
async def delete_post(
    *,
    db: Session = Depends(get_db),
    post_id: int,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """Delete a post"""
    success = BlogService.delete_post(db, post_id, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"success": True}
