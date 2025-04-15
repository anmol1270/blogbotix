from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import httpx
from urllib.parse import urljoin
import logging

from app.core.auth import get_current_active_user
from app.db.base import get_db
from app.models.user import User
from app.schemas.settings import WordPressSettings, WordPressSettingsUpdate

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/wordpress", response_model=WordPressSettings)
def get_wordpress_settings(
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get WordPress settings for the current user.
    """
    return {
        "siteUrl": current_user.wordpress_url,
        "username": current_user.wordpress_username or "",
        "applicationPassword": current_user.wordpress_password or "",
        "postType": "post",
        "postStatus": "draft"
    }

@router.put("/wordpress", response_model=WordPressSettings)
def update_wordpress_settings(
    *,
    db: Session = Depends(get_db),
    settings_in: WordPressSettingsUpdate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Update WordPress settings for the current user.
    """
    logger.info(f"Updating WordPress settings for user {current_user.email}")
    logger.info(f"Received settings: {settings_in}")
    
    try:
        current_user.wordpress_url = str(settings_in.siteUrl) if settings_in.siteUrl else None
        current_user.wordpress_username = settings_in.username
        current_user.wordpress_password = settings_in.applicationPassword
        
        db.add(current_user)
        db.commit()
        db.refresh(current_user)
        
        logger.info(f"Successfully updated settings for user {current_user.email}")
        return {
            "siteUrl": current_user.wordpress_url,
            "username": current_user.wordpress_username or "",
            "applicationPassword": current_user.wordpress_password or "",
            "postType": settings_in.postType,
            "postStatus": settings_in.postStatus
        }
    except Exception as e:
        logger.error(f"Error updating settings: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/wordpress/test")
async def test_wordpress_connection(
    settings_in: WordPressSettingsUpdate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Test WordPress connection with provided settings.
    """
    try:
        # Construct the WordPress REST API URL
        wp_url = str(settings_in.siteUrl).rstrip('/')
        api_url = urljoin(wp_url, '/wp-json/wp/v2/')
        
        # Create basic auth header
        auth = (settings_in.username, settings_in.applicationPassword)
        
        async with httpx.AsyncClient() as client:
            # Try to access the WordPress REST API
            response = await client.get(
                api_url,
                auth=auth,
                timeout=10.0
            )
            
            if response.status_code == 200:
                return {"success": True, "message": "Successfully connected to WordPress"}
            else:
                return {
                    "success": False,
                    "message": f"Failed to connect to WordPress. Status code: {response.status_code}"
                }
                
    except httpx.RequestError as e:
        return {
            "success": False,
            "message": f"Connection error: {str(e)}"
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Error testing connection: {str(e)}"
        } 