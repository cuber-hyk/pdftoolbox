import os
import uuid
import fitz
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from app.core.config import settings


class JobService:
    def __init__(self):
        self.jobs: Dict[str, Dict[str, Any]] = {}

    def create_job(self, tool_id: str, upload_id: str, options: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new processing job."""
        job_id = f'job_{uuid.uuid4().hex[:9]}'
        now = datetime.now()

        job = {
            'job_id': job_id,
            'tool_id': tool_id,
            'upload_id': upload_id,
            'status': 'queued',
            'progress': 0,
            'message': 'Job queued',
            'created_at': now,
            'expires_at': now + timedelta(hours=settings.FILE_EXPIRE_HOURS),
            'options': options,
            'result': None,
            'error': None
        }

        self.jobs[job_id] = job
        return job

    def get_job(self, job_id: str) -> Optional[Dict[str, Any]]:
        """Get job by ID."""
        return self.jobs.get(job_id)

    def update_job(self, job_id: str, **updates) -> None:
        """Update job status."""
        if job_id in self.jobs:
            self.jobs[job_id].update(updates)

    def complete_job(self, job_id: str, result: Dict[str, Any]) -> None:
        """Mark job as completed."""
        if job_id in self.jobs:
            self.jobs[job_id].update({
                'status': 'completed',
                'progress': 100,
                'message': 'Processing complete',
                'completed_at': datetime.now(),
                'result': result
            })

    def fail_job(self, job_id: str, error: Dict[str, Any]) -> None:
        """Mark job as failed."""
        if job_id in self.jobs:
            self.jobs[job_id].update({
                'status': 'failed',
                'message': 'Processing failed',
                'completed_at': datetime.now(),
                'error': error
            })

    def cancel_job(self, job_id: str) -> bool:
        """Cancel a job."""
        job = self.jobs.get(job_id)
        if job and job['status'] in ['queued', 'processing']:
            self.jobs[job_id].update({
                'status': 'cancelled',
                'message': 'Job cancelled'
            })
            return True
        return False


job_service = JobService()
