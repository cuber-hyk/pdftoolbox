"""PDF merge processor."""
from pathlib import Path
from typing import Any, Dict
from datetime import datetime, timedelta
import fitz
from app.processors.base import BaseProcessor
from app.processors.registry import registry
from app.core.config import settings


@registry.register("merge")
class MergeProcessor(BaseProcessor):
    """Processor for merging multiple PDF files."""

    async def process(
        self,
        job_id: str,
        files: list[Path],
        options: Dict[str, Any]
    ) -> str:
        """Merge PDF files.

        Args:
            job_id: Job identifier
            files: List of PDF file paths to merge
            options: Processing options (output_filename)

        Returns:
            Output file ID

        Raises:
            Exception: Merge failed
        """
        from app.services.job_service import job_service

        # Update status
        job_service.update_job(
            job_id,
            status="processing",
            started_at=datetime.now()
        )

        # 生成输出文件名：使用第一个文件名 + "_merged" 或基于时间戳
        if files:
            first_file_name = files[0].stem  # 获取不含扩展名的文件名
            output_filename = f"{first_file_name}_merged.pdf"
        else:
            output_filename = f"merged_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

        output_path = self.get_output_path(job_id, output_filename)

        try:
            result_doc = fitz.open()
            total_files = len(files)

            for i, file_path in enumerate(files):
                # Update progress
                progress = int((i / total_files) * 100)
                self.update_progress(
                    job_id,
                    progress,
                    f"Merging file {i + 1} of {total_files}"
                )

                # Validate and open PDF
                self.validate_pdf(file_path)

                # Insert PDF pages
                with fitz.open(file_path) as doc:
                    result_doc.insert_pdf(doc)

            # Get page count before closing
            page_count = len(result_doc)

            # Save result
            result_doc.save(output_path)
            result_doc.close()

            # Get the actual filename that was saved
            # output_path is like: /path/to/result/{job_id}_merged.pdf
            saved_filename = output_path.name

            # Complete job
            file_size = output_path.stat().st_size
            job_service.complete_job(job_id, {
                "output_file_id": job_id,
                "filename": output_filename,
                "size": file_size,
                "pages": page_count,
                "download_url": f"/api/v1/files/download/{job_id}",
                "expires_at": (datetime.now() + timedelta(hours=settings.FILE_EXPIRE_HOURS)).isoformat()
            })

            return job_id

        except Exception as e:
            job_service.fail_job(job_id, {
                "code": "ERR_MERGE_FAILED",
                "message": str(e)
            })
            raise
