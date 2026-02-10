from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime


class JobCreate(BaseModel):
    tool_id: str
    upload_id: str
    options: dict[str, Any] = {}


class JobResponse(BaseModel):
    job_id: str
    tool_id: str
    upload_id: str
    status: str
    progress: int
    message: str
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    error: Optional[dict[str, Any]] = None
    result: Optional[dict[str, Any]] = None


class JobStatusResponse(BaseModel):
    success: bool = True
    data: JobResponse


class JobCreateResponse(BaseModel):
    success: bool = True
    data: JobResponse
