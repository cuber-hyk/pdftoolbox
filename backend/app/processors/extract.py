"""PDF extract processors."""
from pathlib import Path
from typing import Any, Dict
from datetime import datetime, timedelta
import fitz
from app.processors.base import BaseProcessor
from app.processors.registry import registry
from app.core.config import settings
from app.services.job_service import job_service


@registry.register("extract_pages")
class ExtractPagesProcessor(BaseProcessor):
    """Processor for extracting specific pages from PDF."""

    async def process(
        self,
        job_id: str,
        files: list[Path],
        options: Dict[str, Any]
    ) -> str:
        """Extract specific pages.

        Args:
            job_id: Job identifier
            files: List with single PDF file path
            options: Processing options (pages: "1,3,5-7")

        Returns:
            Output file ID
        """
        # Update status
        job_service.update_job(
            job_id,
            status="processing",
            started_at=datetime.now()
        )

        file_path = files[0]
        pages_str = options.get("pages", "")

        # Parse page specification
        page_indices = self._parse_pages(pages_str)

        # Validate PDF
        doc = self.validate_pdf(file_path)
        total_pages = len(doc)

        # Validate page indices
        for idx in page_indices:
            if idx < 0 or idx >= total_pages:
                raise ValueError(f"Page {idx + 1} does not exist (PDF has {total_pages} pages)")
        doc.close()

        # Update progress
        self.update_progress(job_id, 50, f"Extracting {len(page_indices)} pages")

        # Create new document with selected pages
        new_doc = fitz.open()
        with fitz.open(file_path) as original:
            for idx in page_indices:
                new_doc.insert_pdf(original, from_page=idx, to_page=idx)

        output_path = self.get_output_path(job_id, "extracted_pages.pdf")
        new_doc.save(output_path)
        new_doc.close()

        # Complete job
        file_size = output_path.stat().st_size
        job_service.complete_job(job_id, {
            "output_file_id": job_id,
            "filename": "extracted_pages.pdf",
            "size": file_size,
            "pages": len(page_indices),
            "download_url": f"/api/v1/files/download/{job_id}",
            "expires_at": (datetime.now() + timedelta(hours=settings.FILE_EXPIRE_HOURS)).isoformat()
        })

        return job_id

    def _parse_pages(self, pages_str: str) -> list[int]:
        """Parse page specification string.

        Args:
            pages_str: Page spec like "1,3,5-7"

        Returns:
            List of zero-based page indices

        Raises:
            ValueError: Invalid page specification
        """
        if not pages_str:
            raise ValueError("Page specification is required")

        indices = []
        parts = pages_str.split(',')

        for part in parts:
            part = part.strip()
            if '-' in part:
                # Range like "5-7"
                start, end = part.split('-')
                start = int(start.strip())
                end = int(end.strip())
                indices.extend(range(start - 1, end))
            else:
                # Single page
                indices.append(int(part) - 1)

        return sorted(set(indices))


@registry.register("extract_text")
class ExtractTextProcessor(BaseProcessor):
    """Processor for extracting text from PDF."""

    async def process(
        self,
        job_id: str,
        files: list[Path],
        options: Dict[str, Any]
    ) -> str:
        """Extract text content.

        Args:
            job_id: Job identifier
            files: List with single PDF file path
            options: Processing options (format: "txt" or "json")

        Returns:
            Output file ID
        """
        # Update status
        job_service.update_job(
            job_id,
            status="processing",
            started_at=datetime.now()
        )

        file_path = files[0]
        output_format = options.get("format", "txt")

        # Validate PDF
        doc = self.validate_pdf(file_path)
        total_pages = len(doc)

        # Extract text
        all_text = []
        for i in range(total_pages):
            # Update progress
            progress = int((i / total_pages) * 100)
            self.update_progress(
                job_id,
                progress,
                f"Extracting text from page {i + 1}"
            )

            page = doc[i]
            text = page.get_text()
            all_text.append(text)

        doc.close()

        # Determine output file
        if output_format == "json":
            import json
            content = json.dumps({
                "pages": len(all_text),
                "text": all_text
            }, ensure_ascii=False, indent=2)
            output_filename = "extracted_text.json"
        else:
            content = "\n\n".join(all_text)
            output_filename = "extracted_text.txt"

        # Save to file
        output_path = self.get_output_path(job_id, output_filename)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)

        # Complete job
        file_size = output_path.stat().st_size
        job_service.complete_job(job_id, {
            "output_file_id": job_id,
            "filename": output_filename,
            "size": file_size,
            "download_url": f"/api/v1/files/download/{job_id}",
            "expires_at": (datetime.now() + timedelta(hours=settings.FILE_EXPIRE_HOURS)).isoformat()
        })

        return job_id


@registry.register("extract_images")
class ExtractImagesProcessor(BaseProcessor):
    """Processor for extracting images from PDF."""

    async def process(
        self,
        job_id: str,
        files: list[Path],
        options: Dict[str, Any]
    ) -> str:
        """Extract images from PDF.

        Args:
            job_id: Job identifier
            files: List with single PDF file path
            options: Processing options

        Returns:
            Output file ID
        """
        # Update status
        job_service.update_job(
            job_id,
            status="processing",
            started_at=datetime.now()
        )

        file_path = files[0]
        output_format = options.get("format", "png")

        # Validate PDF
        doc = self.validate_pdf(file_path)
        total_pages = len(doc)

        # Create output directory
        output_dir = Path(settings.RESULT_DIR) / job_id
        output_dir.mkdir(parents=True, exist_ok=True)

        image_count = 0
        for i in range(total_pages):
            # Update progress
            progress = int((i / total_pages) * 100)
            self.update_progress(
                job_id,
                progress,
                f"Extracting images from page {i + 1}"
            )

            page = doc[i]
            image_list = page.get_images()

            for img_index, img in enumerate(image_list):
                xref = img[0]
                base_image = doc.extract_image(xref)

                # Save image
                image_ext = base_image["ext"]
                image_filename = f"page_{i + 1}_img_{img_index + 1}.{image_ext}"
                image_path = output_dir / image_filename

                with open(image_path, "wb") as f:
                    f.write(base_image["image"])

                image_count += 1

        doc.close()

        # For now, return a text file with image info
        # TODO: Return ZIP with all images
        output_path = self.get_output_path(job_id, "images_info.txt")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"Extracted {image_count} images from {total_pages} pages\n")

        # Complete job
        file_size = output_path.stat().st_size
        job_service.complete_job(job_id, {
            "output_file_id": job_id,
            "filename": "images_info.txt",
            "size": file_size,
            "download_url": f"/api/v1/files/download/{job_id}",
            "expires_at": (datetime.now() + timedelta(hours=settings.FILE_EXPIRE_HOURS)).isoformat()
        })

        return job_id
