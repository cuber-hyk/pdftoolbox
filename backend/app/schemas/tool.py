from pydantic import BaseModel
from typing import Any, Optional


class ToolOption(BaseModel):
    name: str
    type: str = 'string'
    label: str
    description: Optional[str] = None
    placeholder: Optional[str] = None
    default: Optional[Any] = None
    required: Optional[bool] = False
    min: Optional[float] = None
    max: Optional[float] = None
    suffix: Optional[str] = None
    options: Optional[list[dict[str, str]]] = None
    visible_when: Optional[dict[str, str]] = None
    accept: Optional[list[str]] = None


class Tool(BaseModel):
    id: str
    name: str
    description: str
    icon: str
    route: str
    category: str
    max_files: int
    max_size_mb: int
    max_total_size_mb: int
    options: list[ToolOption] = []


class ToolResponse(BaseModel):
    success: bool = True
    data: list[Tool]


class ToolDetailResponse(BaseModel):
    success: bool = True
    data: Tool
