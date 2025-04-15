from sqlalchemy.orm import relationship
from app.models.user import User
from app.models.blog import BlogPost

# Add back_populates relationships
User.blog_posts = relationship("BlogPost", back_populates="user")

__all__ = ["User", "BlogPost"]
