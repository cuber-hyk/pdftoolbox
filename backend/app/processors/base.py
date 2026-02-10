"""Base processor for PDF operations."""
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict
from datetime import datetime
import fitz


class BaseProcessor(ABC):
    """Base class for PDF processors."""

    def __init__(self, job_service):
        """Initialize processor with job service.

        Args:
            job_service: Job service instance for status updates
        """
        self.job_service = job_service

    @abstractmethod
    async def process(
        self,
        job_id: str,
        files: list[Path],
        options: Dict[str, Any]
    ) -> str:
        """Process PDF files.

        Args:
            job_id: Job identifier
            files: List of input file paths
            options: Processing options

        Returns:
            Output file ID

        Raises:
            Exception: Processing failed
        """
        pass

    def validate_pdf(self, file_path: Path) -> fitz.Document:
        """Validate and open PDF file.

        Args:
            file_path: Path to PDF file

        Returns:
            PyMuPDF document

        Raises:
            ValueError: Invalid PDF file
        """
        try:
            doc = fitz.open(file_path)
            if doc.is_encrypted:
                raise ValueError("PDF file is encrypted and not supported")
            if len(doc) == 0:
                raise ValueError("PDF file has no pages")
            return doc
        except Exception as e:
            raise ValueError(f"Invalid PDF file: {e}")

    def get_page_count(self, file_path: Path) -> int:
        """Get PDF page count.

        Args:
            file_path: Path to PDF file

        Returns:
            Number of pages
        """
        doc = fitz.open(file_path)
        count = len(doc)
        doc.close()
        return count

    def get_output_path(self, job_id: str, filename: str) -> Path:
        """Get output file path.

        Args:
            job_id: Job identifier
            filename: Output filename

        Returns:
            Output file path
        """
        from app.core.config import settings
        output_dir = Path(settings.RESULT_DIR)
        output_dir.mkdir(parents=True, exist_ok=True)
        return output_dir / f"{job_id}_{filename}"

    def update_progress(
        self,
        job_id: str,
        progress: int,
        message: str
    ) -> None:
        """Update job progress.

        Args:
            job_id: Job identifier
            progress: Progress percentage (0-100)
            message: Progress message
        """
        self.job_service.update_job(
            job_id,
            progress=progress,
            message=message
        )
