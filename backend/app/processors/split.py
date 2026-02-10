"""PDF split processor."""
from pathlib import Path
from typing import Any, Dict
from datetime import datetime, timedelta
import zipfile
import fitz
from app.processors.base import BaseProcessor
from app.processors.registry import registry
from app.core.config import settings
from app.services.job_service import job_service


@registry.register("split")
class SplitProcessor(BaseProcessor):
    """Processor for splitting PDF files."""

    async def process(
        self,
        job_id: str,
        files: list[Path],
        options: Dict[str, Any]
    ) -> str:
        """Split PDF file.

        Args:
            job_id: Job identifier
            files: List with single PDF file path
            options: Processing options (mode, ranges, every_n_pages)

        Returns:
            Output file ID

        Raises:
            Exception: Split failed
        """
        print(f"[DEBUG] SplitProcessor.process called: job_id={job_id}, files={files}, options={options}")

        # Update status
        job_service.update_job(
            job_id,
            status="processing",
            started_at=datetime.now()
        )

        mode = options.get("mode", "range")
        file_path = files[0]

        print(f"[DEBUG] Mode: {mode}")

        if mode == "range":
            print(f"[DEBUG] Calling _split_by_range")
            return await self._split_by_range(job_id, file_path, options)
        elif mode == "every":
            print(f"[DEBUG] Calling _split_by_every")
            return await self._split_by_every(job_id, file_path, options)
        elif mode == "single":
            print(f"[DEBUG] Calling _split_into_singles")
            return await self._split_into_singles(job_id, file_path, options)
        else:
            raise ValueError(f"Unsupported split mode: {mode}")

    async def _split_by_range(
        self,
        job_id: str,
        file_path: Path,
        options: Dict[str, Any]
    ) -> str:
        """Split PDF by page ranges.

        Args:
            job_id: Job identifier
            file_path: PDF file path
            options: Range options (ranges: string like "1-3, 5-7, 9-10")

        Returns:
            Output file ID
        """
        # Parse ranges string (e.g., "1-3, 5-7, 9-10")
        ranges_str = options.get("ranges", "1-1")
        ranges = self._parse_ranges(ranges_str)

        # Validate input file
        doc = self.validate_pdf(file_path)
        total_pages = len(doc)
        doc.close()

        # Create output directory for split files
        output_dir = Path(settings.RESULT_DIR) / job_id
        output_dir.mkdir(parents=True, exist_ok=True)

        output_files = []

        for i, (start, end) in enumerate(ranges):
            # Adjust end page if -1
            if end == -1:
                end = total_pages

            # Validate range
            if start < 1 or end > total_pages or start > end:
                raise ValueError(f"Invalid page range: {start}-{end}")

            # Update progress
            progress = int((i / len(ranges)) * 100)
            self.update_progress(
                job_id,
                progress,
                f"Creating part {i + 1} (pages {start}-{end})"
            )

            # Create new document with selected pages
            new_doc = fitz.open()
            with fitz.open(file_path) as original:
                new_doc.insert_pdf(original, from_page=start - 1, to_page=end - 1)

            output_path = output_dir / f"part_{i + 1}.pdf"
            new_doc.save(output_path)
            new_doc.close()
            output_files.append(output_path)

        # Create ZIP file with all split files
        return await self._create_zip_package(job_id, output_files, "split_pages.zip")

    async def _split_by_every(
        self,
        job_id: str,
        file_path: Path,
        options: Dict[str, Any]
    ) -> str:
        """Split PDF every N pages.

        Args:
            job_id: Job identifier
            file_path: PDF file path
            options: Every N pages options

        Returns:
            Output file ID
        """
        every_n = options.get("every_n", 2)

        doc = self.validate_pdf(file_path)
        total_pages = len(doc)
        doc.close()

        # Create output directory for split files
        output_dir = Path(settings.RESULT_DIR) / job_id
        output_dir.mkdir(parents=True, exist_ok=True)

        output_files = []
        part_num = 1
        start_page = 0

        while start_page < total_pages:
            end_page = min(start_page + every_n, total_pages)

            # Update progress
            progress = int((start_page / total_pages) * 100)
            self.update_progress(
                job_id,
                progress,
                f"Creating part {part_num} (pages {start_page + 1}-{end_page})"
            )

            # Create new document
            new_doc = fitz.open()
            with fitz.open(file_path) as original:
                new_doc.insert_pdf(original, from_page=start_page, to_page=end_page - 1)

            output_path = output_dir / f"part_{part_num}.pdf"
            new_doc.save(output_path)
            new_doc.close()
            output_files.append(output_path)

            start_page = end_page
            part_num += 1

        # Create ZIP file with all split files
        return await self._create_zip_package(job_id, output_files, f"split_every_{every_n}.zip")

    async def _split_into_singles(
        self,
        job_id: str,
        file_path: Path,
        options: Dict[str, Any]
    ) -> str:
        """Split PDF into single pages.

        Args:
            job_id: Job identifier
            file_path: PDF file path
            options: Options

        Returns:
            Output file ID
        """
        print(f"[DEBUG] _split_into_singles called with job_id: {job_id}, file_path: {file_path}")

        doc = self.validate_pdf(file_path)
        total_pages = len(doc)
        doc.close()

        print(f"[DEBUG] Total pages in PDF: {total_pages}")

        if total_pages <= 1:
            raise ValueError(f"PDF file has only {total_pages} page(s). Cannot split into single pages. Please use a multi-page PDF file.")

        # Create output directory for split files
        output_dir = Path(settings.RESULT_DIR) / job_id
        output_dir.mkdir(parents=True, exist_ok=True)

        print(f"[DEBUG] Output directory: {output_dir}")

        output_files = []

        for i in range(total_pages):
            # Update progress
            progress = int((i / total_pages) * 100)
            self.update_progress(
                job_id,
                progress,
                f"Creating page {i + 1}"
            )

            # Create new document with single page
            new_doc = fitz.open()
            with fitz.open(file_path) as original:
                new_doc.insert_pdf(original, from_page=i, to_page=i)

            output_path = output_dir / f"page_{i + 1}.pdf"
            new_doc.save(output_path)
            new_doc.close()
            output_files.append(output_path)
            print(f"[DEBUG] Created: {output_path}")

        print(f"[DEBUG] Total files created: {len(output_files)}")
        print(f"[DEBUG] Calling _create_zip_package...")

        # Create ZIP file with all single pages
        result = await self._create_zip_package(job_id, output_files, "single_pages.zip")

        print(f"[DEBUG] _create_zip_package returned: {result}")
        return result

    async def _create_zip_package(
        self,
        job_id: str,
        file_paths: list[Path],
        zip_filename: str
    ) -> str:
        """Create a ZIP package from multiple PDF files.

        Args:
            job_id: Job identifier
            file_paths: List of PDF file paths to include
            zip_filename: Name for the ZIP file

        Returns:
            Output file ID (job_id)
        """
        # Create ZIP file path
        zip_path = self.get_output_path(job_id, zip_filename)

        print(f"[DEBUG] Creating ZIP: {zip_path}")
        print(f"[DEBUG] Input files: {file_paths}")

        # Create ZIP file
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in file_paths:
                if file_path.exists():
                    print(f"[DEBUG] Adding to ZIP: {file_path}")
                    # Add file to ZIP with just the filename (not full path)
                    zipf.write(file_path, file_path.name)
                else:
                    print(f"[DEBUG] File not found: {file_path}")

        # Verify ZIP was created
        if not zip_path.exists():
            raise RuntimeError(f"Failed to create ZIP file: {zip_path}")

        # Get ZIP file size
        file_size = zip_path.stat().st_size
        print(f"[DEBUG] ZIP created: {zip_path}, size: {file_size}")

        # Complete job with ZIP file info
        job_service.complete_job(job_id, {
            "output_file_id": job_id,
            "filename": zip_filename,
            "size": file_size,
            "file_count": len(file_paths),
            "download_url": f"/api/v1/files/download/{job_id}",
            "expires_at": (datetime.now() + timedelta(hours=settings.FILE_EXPIRE_HOURS)).isoformat()
        })

        return job_id

    def _parse_ranges(self, ranges_str: str) -> list[tuple[int, int]]:
        """Parse ranges string into list of tuples.

        Args:
            ranges_str: Ranges string like "1-3, 5-7, 9-10" or "1-3,5--1"

        Returns:
            List of (start, end) tuples. -1 means last page.

        Raises:
            ValueError: Invalid range format
        """
        if not ranges_str:
            raise ValueError("Page ranges are required")

        ranges = []
        parts = ranges_str.split(',')

        for part in parts:
            part = part.strip()
            if '-' in part:
                start, end = part.split('-', 1)
                start = int(start.strip())
                end = int(end.strip())
                ranges.append((start, end))
            else:
                # Single page
                page = int(part)
                ranges.append((page, page))

        if not ranges:
            raise ValueError("At least one valid range is required")

        return ranges

