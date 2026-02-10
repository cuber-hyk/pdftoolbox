from fastapi import APIRouter, HTTPException
from app.schemas.tool import ToolResponse, ToolDetailResponse
from app.models.tools import TOOLS_DB
from typing import Any

router = APIRouter()


@router.get('', response_model=ToolResponse)
async def get_tools():
    """Get all available PDF tools."""
    return ToolResponse(data=TOOLS_DB)


@router.get('/{tool_id}', response_model=ToolDetailResponse)
async def get_tool(tool_id: str):
    """Get tool details by ID."""
    tool = next((t for t in TOOLS_DB if t['id'] == tool_id), None)
    if not tool:
        raise HTTPException(status_code=404, detail='Tool not found')
    return ToolDetailResponse(data=tool)
