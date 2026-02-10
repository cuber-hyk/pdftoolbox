"""Background task processing service."""
import asyncio
from pathlib import Path
from typing import Dict, Any
from app.services.job_service import job_service
from app.processors.registry import registry
from app.core.config import settings


class TaskProcessor:
    """Service for running PDF processing tasks in background."""

    def __init__(self):
        """Initialize task processor."""
        self.running_tasks: Dict[str, asyncio.Task] = {}

    async def process_job(
        self,
        job_id: str,
        tool_id: str,
        upload_id: str,
        options: Dict[str, Any]
    ) -> None:
        """Process a job in background.

        Args:
            job_id: Job identifier
            tool_id: Tool identifier
            upload_id: Upload identifier
            options: Processing options
        """
        try:
            print(f"[DEBUG] process_job called: job_id={job_id}, tool_id={tool_id}, upload_id={upload_id}, options={options}")

            # Get processor
            processor_class = registry.get(tool_id)
            if not processor_class:
                raise ValueError(f"Unknown tool: {tool_id}")

            # Initialize processor
            processor = processor_class(job_service)

            # Get uploaded files
            file_paths = self._get_uploaded_files(upload_id)
            print(f"[DEBUG] Found {len(file_paths)} files to process")

            # Process files
            result = await processor.process(job_id, file_paths, options)
            print(f"[DEBUG] Processor returned: {result}")

        except Exception as e:
            print(f"[DEBUG] Error in process_job: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            job_service.fail_job(job_id, {
                "code": "ERR_PROCESSING_FAILED",
                "message": str(e)
            })

    def _get_uploaded_files(self, upload_id: str) -> list[Path]:
        """Get list of uploaded file paths.

        Args:
            upload_id: Upload identifier

        Returns:
            List of file paths

        Raises:
            ValueError: Upload directory not found
        """
        import os

        upload_dir = Path(settings.UPLOAD_DIR)

        # Find all files matching the upload_id prefix: {upload_id}_*.pdf
        files = []
        if upload_dir.exists():
            for file_path in sorted(upload_dir.glob(f"{upload_id}_*.pdf")):
                files.append(file_path)

        if not files:
            raise ValueError(f"No files found for upload: {upload_id}")

        return files

    def create_task(
        self,
        job_id: str,
        tool_id: str,
        upload_id: str,
        options: Dict[str, Any]
    ) -> None:
        """Create background task for job processing.

        Args:
            job_id: Job identifier
            tool_id: Tool identifier
            upload_id: Upload identifier
            options: Processing options
        """
        # Create async task
        loop = asyncio.get_event_loop()
        task = loop.create_task(
            self.process_job(job_id, tool_id, upload_id, options)
        )

        self.running_tasks[job_id] = task

    def get_task_status(self, job_id: str) -> str:
        """Get status of running task.

        Args:
            job_id: Job identifier

        Returns:
            Task status
        """
        job = job_service.get_job(job_id)
        if job:
            return job.get('status', 'unknown')
        return 'unknown'


# Global instance
task_processor = TaskProcessor()
