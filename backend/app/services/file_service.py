import os
import uuid
import fitz
from datetime import datetime, timedelta
from typing import Optional
from fastapi import UploadFile, HTTPException
from app.core.config import settings


class FileService:
    def __init__(self):
        self.ensure_directories()

    def ensure_directories(self):
        """Ensure storage directories exist."""
        os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
        os.makedirs(settings.RESULT_DIR, exist_ok=True)

    def generate_file_id(self) -> str:
        """Generate unique file ID."""
        return f'f_{uuid.uuid4().hex[:12]}'

    def generate_upload_id(self) -> str:
        """Generate unique upload ID."""
        return f'ul_{uuid.uuid4().hex[:12]}'

    def get_file_path(self, file_id: str) -> str:
        """Get file path from file ID."""
        return os.path.join(settings.UPLOAD_DIR, f'{file_id}.pdf')

    def get_expires_at(self) -> datetime:
        """Get file expiration time."""
        return datetime.now() + timedelta(hours=settings.FILE_EXPIRE_HOURS)

    async def save_uploaded_file(self, file: UploadFile, file_id: str) -> dict:
        """Save uploaded file and return metadata."""
        file_path = self.get_file_path(file_id)

        try:
            # Save file
            with open(file_path, 'wb') as f:
                content = await file.read()
                f.write(content)

            # Get PDF metadata
            doc = fitz.open(file_path)
            pages = len(doc)
            metadata = doc.metadata
            doc.close()

            return {
                'file_id': file_id,
                'name': file.filename or 'unknown.pdf',
                'size': len(content),
                'pages': pages,
                'metadata': {
                    'title': metadata.get('title'),
                    'author': metadata.get('author'),
                    'created': metadata.get('creationDate')
                }
            }
        except Exception as e:
            # Clean up file if processing failed
            if os.path.exists(file_path):
                os.remove(file_path)
            raise HTTPException(status_code=400, detail=f'Invalid PDF file: {str(e)}')

    async def save_uploaded_file_with_prefix(
        self, file: UploadFile, file_id: str, upload_id: str
    ) -> dict:
        """Save uploaded file with upload_id prefix and return metadata."""
        # File format: {upload_id}_{file_id}.pdf
        file_path = os.path.join(settings.UPLOAD_DIR, f'{upload_id}_{file_id}.pdf')

        try:
            # Save file
            with open(file_path, 'wb') as f:
                content = await file.read()
                f.write(content)

            # Get PDF metadata
            doc = fitz.open(file_path)
            pages = len(doc)
            metadata = doc.metadata
            doc.close()

            return {
                'file_id': file_id,
                'name': file.filename or 'unknown.pdf',
                'size': len(content),
                'pages': pages,
                'metadata': {
                    'title': metadata.get('title'),
                    'author': metadata.get('author'),
                    'created': metadata.get('creationDate')
                }
            }
        except Exception as e:
            # Clean up file if processing failed
            if os.path.exists(file_path):
                os.remove(file_path)
            raise HTTPException(status_code=400, detail=f'Invalid PDF file: {str(e)}')

    async def save_uploaded_file_with_index(
        self, file: UploadFile, file_id: str, upload_id: str, index: int
    ) -> dict:
        """Save uploaded file with upload_id and index prefix.

        File format: {upload_id}_{index:04d}_{file_id}.pdf
        This ensures files are sorted by upload order when using glob().
        """
        # File format: {upload_id}_{index:04d}_{file_id}.pdf
        # Example: ul_abc123_0000_f_def456.pdf
        file_path = os.path.join(settings.UPLOAD_DIR, f'{upload_id}_{index:04d}_{file_id}.pdf')

        try:
            # Save file
            with open(file_path, 'wb') as f:
                content = await file.read()
                f.write(content)

            # Get PDF metadata
            doc = fitz.open(file_path)
            pages = len(doc)
            metadata = doc.metadata
            doc.close()

            return {
                'file_id': file_id,
                'index': index,  # 保存索引用于前端显示和删除
                'name': file.filename or 'unknown.pdf',
                'size': len(content),
                'pages': pages,
                'metadata': {
                    'title': metadata.get('title'),
                    'author': metadata.get('author'),
                    'created': metadata.get('creationDate')
                }
            }
        except Exception as e:
            # Clean up file if processing failed
            if os.path.exists(file_path):
                os.remove(file_path)
            raise HTTPException(status_code=400, detail=f'Invalid PDF file: {str(e)}')

    def validate_file(self, file: UploadFile) -> None:
        """Validate uploaded file."""
        # Check file type
        if file.content_type not in settings.ALLOWED_FILE_TYPES:
            raise HTTPException(
                status_code=415,
                detail=f'Invalid file type. Allowed: {settings.ALLOWED_FILE_TYPES}'
            )

        # Check file size
        content = file.file.read()
        file.file.seek(0)
        if len(content) > settings.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413,
                detail=f'File too large. Max size: {settings.MAX_FILE_SIZE / 1024 / 1024}MB'
            )

    def delete_file(self, file_id: str) -> bool:
        """Delete file by ID."""
        file_path = self.get_file_path(file_id)
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False

    def delete_file_with_prefix(self, filename: str) -> bool:
        """Delete file by full filename (with prefix)."""
        file_path = os.path.join(settings.UPLOAD_DIR, filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False


file_service = FileService()
