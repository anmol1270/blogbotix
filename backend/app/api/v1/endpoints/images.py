from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict

from app.db.base import get_db
from app.core.auth import get_current_user
from app.models.user import User
from app.services.image_generator import ImageGenerator

router = APIRouter()

@router.post("/generate/")
async def generate_image(
    request: Dict[str, str],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Dict[str, str]:
    """
    Generate an image based on the blog post content and title
    
    Args:
        request: Dictionary containing 'content' and 'title'
    """
    try:
        if not request.get("content") or not request.get("title"):
            raise HTTPException(
                status_code=400,
                detail="Both content and title are required"
            )
            
        image_url = await ImageGenerator.generate_image(
            content=request["content"],
            title=request["title"]
        )
        return {"imageUrl": image_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 