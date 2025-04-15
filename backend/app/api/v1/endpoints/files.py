from fastapi import APIRouter, UploadFile, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from typing import Dict, List, Optional

from app.services.file_processor import FileProcessor
from app.db.base import get_db
from app.core.auth import get_current_user
from app.models.user import User

router = APIRouter()

@router.post("/upload/")
async def upload_file(
    file: UploadFile,
    custom_prompt: Optional[str] = Form(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Dict[str, str | List[str]]:
    """
    Upload a Word or PDF file and extract its content
    
    Args:
        file: The uploaded file
        custom_prompt: Optional custom prompt for GPT-4 processing
    """
    try:
        result = await FileProcessor.process_file(file, custom_prompt)
        return result
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 