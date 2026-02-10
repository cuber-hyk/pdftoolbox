"""Job API endpoints."""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from app.schemas.job import JobCreateResponse, JobStatusResponse
from app.services.job_service import job_service
from app.services.task_processor import task_processor
from app.models.tools import TOOLS_DB
from app.processors.registry import registry
from typing import Any

router = APIRouter()


@router.post('', response_model=JobCreateResponse)
async def create_job(
    job_data: dict[str, Any],
    background_tasks: BackgroundTasks
):
    """Create a new PDF processing job."""
    # Validate tool exists
    tool = next((t for t in TOOLS_DB if t['id'] == job_data.get('tool_id')), None)
    if not tool:
        raise HTTPException(status_code=404, detail='Tool not found')

    # Check if processor exists
    if not registry.exists(job_data.get('tool_id')):
        raise HTTPException(
            status_code=400,
            detail=f'Tool processor not implemented: {job_data.get("tool_id")}'
        )

    # Create job
    job = job_service.create_job(
        tool_id=job_data.get('tool_id'),
        upload_id=job_data.get('upload_id'),
        options=job_data.get('options', {})
    )

    # Start background processing
    background_tasks.add_task(
        task_processor.process_job,
        job['job_id'],
        job_data.get('tool_id'),
        job_data.get('upload_id'),
        job_data.get('options', {})
    )

    return JobCreateResponse(data=job)


@router.get('/{job_id}', response_model=JobStatusResponse)
async def get_job_status(job_id: str):
    """Get job status."""
    job = job_service.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail='Job not found')

    return JobStatusResponse(data=job)


@router.delete('/{job_id}')
async def cancel_job(job_id: str):
    """Cancel a job."""
    success = job_service.cancel_job(job_id)
    if not success:
        raise HTTPException(status_code=400, detail='Cannot cancel job')

    return {'success': True, 'message': 'Job cancelled'}
