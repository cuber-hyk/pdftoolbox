from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class FileMetadata(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    created: Optional[str] = None


class FileInfo(BaseModel):
    file_id: str
    name: str
    size: int
    pages: Optional[int] = None
    metadata: Optional[FileMetadata] = None
    is_encrypted: Optional[bool] = False


class UploadResponse(BaseModel):
    success: bool = True
    data: "UploadData"


class UploadData(BaseModel):
    upload_id: str
    files: list[FileInfo]
    total_size: int
    expires_at: datetime


class ErrorResponse(BaseModel):
    success: bool = False
    error: "ErrorDetail"


class ErrorDetail(BaseModel):
    code: str
    message: str
    details: Optional[dict] = None
