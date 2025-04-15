from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.blog import BlogPost
from app.models.user import User
from app.schemas.blog import BlogPostCreate, BlogPostUpdate
from app.services.wordpress import WordPressService
import logging

logger = logging.getLogger(__name__)

class BlogService:
    @staticmethod
    async def create_post(db: Session, post: BlogPostCreate, user_id: int) -> BlogPost:
        """Create a new blog post"""
        db_post = BlogPost(
            title=post.title,
            content=post.content,
            summary=post.summary,
            keywords=post.keywords,
            image_url=post.image_url,
            status=post.status or "draft",
            user_id=user_id
        )
        db.add(db_post)
        db.commit()
        db.refresh(db_post)
        return db_post

    @staticmethod
    async def update_post(
        db: Session,
        post_id: int,
        post: BlogPostUpdate,
        user_id: int
    ) -> BlogPost:
        """Update an existing blog post"""
        db_post = db.query(BlogPost).filter(
            BlogPost.id == post_id,
            BlogPost.user_id == user_id
        ).first()
        
        if not db_post:
            raise Exception("Post not found")
            
        for field, value in post.dict(exclude_unset=True).items():
            setattr(db_post, field, value)
            
        db.commit()
        db.refresh(db_post)
        return db_post

    @staticmethod
    async def publish_post(db: Session, post_id: int, user_id: int) -> BlogPost:
        """Publish a blog post to WordPress"""
        db_post = db.query(BlogPost).filter(
            BlogPost.id == post_id,
            BlogPost.user_id == user_id
        ).first()
        
        if not db_post:
            raise Exception("Post not found")
            
        # Get the user
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise Exception("User not found")
            
        try:
            # Publish to WordPress
            wordpress_id = await WordPressService.publish_post(
                title=db_post.title,
                content=db_post.content,
                user=user,
                image_url=db_post.image_url
            )
            
            # Update the post with WordPress ID and status
            db_post.wordpress_post_id = wordpress_id
            db_post.status = "published"
            db.commit()
            db.refresh(db_post)
            
            return db_post
            
        except Exception as e:
            logger.error(f"Error publishing post to WordPress: {str(e)}")
            raise Exception(f"Failed to publish post: {str(e)}")

    @staticmethod
    def get_post(db: Session, post_id: int, user_id: int) -> Optional[BlogPost]:
        """Get a blog post by ID"""
        return db.query(BlogPost).filter(
            BlogPost.id == post_id,
            BlogPost.user_id == user_id
        ).first()

    @staticmethod
    def get_user_posts(db: Session, user_id: int) -> List[BlogPost]:
        """Get all posts for a user"""
        return db.query(BlogPost).filter(BlogPost.user_id == user_id).all()

    @staticmethod
    def delete_post(db: Session, post_id: int, user_id: int) -> bool:
        """Delete a blog post"""
        db_post = db.query(BlogPost).filter(
            BlogPost.id == post_id,
            BlogPost.user_id == user_id
        ).first()
        
        if not db_post:
            return False
            
        db.delete(db_post)
        db.commit()
        return True
