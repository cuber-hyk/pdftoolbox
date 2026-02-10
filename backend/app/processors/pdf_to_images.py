"""PDF to images converter processor."""
import io
from pathlib import Path
from typing import Any, Dict, List
from datetime import datetime, timedelta
import zipfile
import fitz
from PIL import Image
from app.processors.base import BaseProcessor
from app.processors.registry import registry
from app.core.config import settings
from app.services.job_service import job_service


@registry.register("pdf_to_images")
class PdfToImagesProcessor(BaseProcessor):
    """Processor for converting PDF pages to images."""

    async def process(
        self,
        job_id: str,
        files: list[Path],
        options: Dict[str, Any]
    ) -> str:
        """Convert PDF pages to images."""
        job_service.update_job(
            job_id,
            status="processing",
            started_at=datetime.now()
        )

        file_path = files[0]

        # Get options
        mode = options.get("mode", "all")
        output_format = options.get("format", "png")
        dpi = int(options.get("dpi", 150))

        # Validate output format
        format_map = {
            "png": "PNG",
            "jpg": "JPEG",
            "webp": "WebP"
        }
        if output_format not in format_map:
            raise ValueError(f"Invalid format: {output_format}")
        pil_format = format_map[output_format]

        # Get file extension for output
        ext_map = {
            "png": ".png",
            "jpg": ".jpg",
            "webp": ".webp"
        }
        file_ext = ext_map[output_format]

        doc = self.validate_pdf(file_path)
        total_pages = len(doc)

        # Determine which pages to convert
        if mode == "all":
            page_indices = list(range(total_pages))
        elif mode == "range":
            ranges_str = options.get("ranges", "")
            page_indices = self._parse_ranges(ranges_str, total_pages)
        elif mode == "single":
            page_num = int(options.get("page", 1))
            page_indices = [page_num - 1] if 0 < page_num - 1 < total_pages else []
        else:
            page_indices = list(range(total_pages))

        if not page_indices:
            raise ValueError("No valid pages selected")

        self.update_progress(job_id, 10, f"Converting {len(page_indices)} pages...")

        # Create output directory for this job
        output_dir = Path(settings.RESULT_DIR) / job_id
        output_dir.mkdir(parents=True, exist_ok=True)

        # Get PDF filename for naming images
        pdf_name = file_path.stem
        output_files = []

        # Convert each page
        for idx, page_num in enumerate(page_indices):
            progress = int(10 + (idx / len(page_indices)) * 75)
            self.update_progress(job_id, progress, f"Converting page {page_num + 1}...")

            page = doc[page_num]
            mat = fitz.Matrix(dpi / 72, dpi / 72)

            # Render page to pixmap
            pix = page.get_pixmap(matrix=mat, alpha=(output_format == "png"))

            # Convert to PIL Image
            img_bytes = pix.tobytes("ppm")
            pil_img = Image.open(io.BytesIO(img_bytes))

            # Ensure RGB mode for JPG
            if output_format == "jpg" and pil_img.mode != "RGB":
                pil_img = pil_img.convert("RGB")

            # Save image
            output_filename = f"{pdf_name}_page_{page_num + 1:04d}{file_ext}"
            output_path = output_dir / output_filename
            pil_img.save(output_path, format=pil_format, quality=95)
            output_files.append(output_filename)

            pix = None  # Free memory

        doc.close()

        # Create ZIP file
        self.update_progress(job_id, 90, "Creating ZIP archive...")
        zip_path = Path(settings.RESULT_DIR) / f"{job_id}_images.zip"

        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for filename in output_files:
                file_path = output_dir / filename
                zipf.write(file_path, filename)

        # Clean up individual image files
        for filename in output_files:
            (output_dir / filename).unlink()
        output_dir.rmdir()

        file_size = zip_path.stat().st_size
        job_service.complete_job(job_id, {
            "output_file_id": f"{job_id}_images",
            "filename": f"{pdf_name}_images.zip",
            "size": file_size,
            "pages": total_pages,
            "converted_pages": len(page_indices),
            "format": output_format,
            "dpi": dpi,
            "download_url": f"/api/v1/files/download/{job_id}_images",
            "expires_at": (datetime.now() + timedelta(hours=settings.FILE_EXPIRE_HOURS)).isoformat()
        })

        return f"{job_id}_images"

    def _parse_ranges(self, ranges_str: str, total_pages: int) -> list[int]:
        """Parse page range string.

        Args:
            ranges_str: Range string like "1-3, 5-7"
            total_pages: Total number of pages in PDF

        Returns:
            List of page indices (0-based)
        """
        indices = set()

        for part in ranges_str.split(','):
            part = part.strip()
            if not part:
                continue

            if '-' in part:
                if '--' in part:
                    # "N--" means from N to end
                    start = int(part.split('--')[0]) - 1
                    indices.update(range(max(0, start), total_pages))
                else:
                    # "N-M" range
                    try:
                        start, end = part.split('-')
                        start = int(start) - 1
                        end = int(end) - 1
                        indices.update(range(max(0, start), min(total_pages, end + 1)))
                    except ValueError:
                        # Skip invalid range
                        continue
            else:
                # Single page
                try:
                    page = int(part) - 1
                    if 0 <= page < total_pages:
                        indices.add(page)
                except ValueError:
                    # Skip invalid page number
                    continue

        return sorted(indices)
