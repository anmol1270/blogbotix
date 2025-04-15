from typing import Dict, Optional
import os
from pathlib import Path
import docx
from PyPDF2 import PdfReader
from fastapi import UploadFile, HTTPException
import tempfile
from app.services.ai import AIService
import logging

# Configure logging
logger = logging.getLogger(__name__)

class FileProcessor:
    ALLOWED_EXTENSIONS = {'.docx', '.pdf'}
    
    @staticmethod
    async def save_upload_file_tmp(upload_file: UploadFile) -> Path:
        """Save uploaded file to a temporary location"""
        try:
            logger.debug(f"Saving uploaded file: {upload_file.filename}")
            suffix = Path(upload_file.filename).suffix
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                content = await upload_file.read()
                tmp.write(content)
                logger.debug(f"File saved to: {tmp.name}")
                return Path(tmp.name)
        except Exception as e:
            logger.error(f"Error saving file: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Could not save file: {str(e)}")

    @staticmethod
    def validate_file_extension(filename: str) -> bool:
        """Validate if file extension is allowed"""
        suffix = Path(filename).suffix.lower()
        if suffix not in FileProcessor.ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"File type not allowed. Allowed types: {', '.join(FileProcessor.ALLOWED_EXTENSIONS)}"
            )
        return True

    @staticmethod
    def extract_text_from_docx(file_path: Path) -> str:
        """Extract text from a Word document"""
        try:
            doc = docx.Document(file_path)
            full_text = []
            for para in doc.paragraphs:
                full_text.append(para.text)
            return '\n\n'.join(full_text)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Could not process Word document: {str(e)}")

    @staticmethod
    def extract_text_from_pdf(file_path: Path) -> str:
        """Extract text from a PDF document"""
        try:
            reader = PdfReader(file_path)
            full_text = []
            for page in reader.pages:
                full_text.append(page.extract_text())
            return '\n\n'.join(full_text)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Could not process PDF document: {str(e)}")

    @staticmethod
    def generate_summary(content: str) -> str:
        """Generate a summary from the content"""
        # For now, just return the first few sentences
        sentences = content.split('.')
        if len(sentences) > 3:
            return '. '.join(sentences[:3]) + '.'
        return content

    @staticmethod
    def extract_keywords(content: str) -> list[str]:
        """Extract keywords from the content"""
        # For now, just return some dummy keywords
        # In a real implementation, you would use NLP to extract meaningful keywords
        return ["keyword1", "keyword2", "keyword3"]

    @classmethod
    async def process_file(cls, file: UploadFile, custom_prompt: Optional[str] = None) -> Dict[str, str]:
        """
        Process uploaded file and extract content
        
        Args:
            file: The uploaded file
            custom_prompt: Optional custom prompt for GPT-4 processing
        """
        logger.debug(f"Processing file: {file.filename}")
        cls.validate_file_extension(file.filename)
        
        temp_file = await cls.save_upload_file_tmp(file)
        try:
            # Extract text from the file
            logger.debug("Extracting text from file")
            if file.filename.lower().endswith('.docx'):
                content = cls.extract_text_from_docx(temp_file)
            else:  # PDF
                content = cls.extract_text_from_pdf(temp_file)
            
            logger.debug(f"Extracted content length: {len(content)}")
            
            # Process content with GPT-4
            logger.debug("Processing content with GPT-4")
            processed_content = await AIService.process_content(content, custom_prompt)
            
            return {
                "filename": file.filename,
                "content": processed_content["content"],
                "title": processed_content["title"],
                "keywords": processed_content["keywords"],
                "summary": processed_content["summary"]
            }
        finally:
            # Clean up temporary file
            try:
                os.unlink(temp_file)
                logger.debug("Temporary file cleaned up")
            except Exception as e:
                logger.error(f"Error cleaning up temporary file: {str(e)}") 