"""PDF watermark processors."""
from pathlib import Path
from typing import Any, Dict
from datetime import datetime, timedelta
import zipfile
import base64
import io
import fitz
from app.processors.base import BaseProcessor
from app.processors.registry import registry
from app.core.config import settings
from app.services.job_service import job_service


@registry.register("add_watermark")
class AddWatermarkProcessor(BaseProcessor):
    """Processor for adding watermarks to PDF."""

    async def process(
        self,
        job_id: str,
        files: list[Path],
        options: Dict[str, Any]
    ) -> str:
        """Add watermark to PDF.

        Args:
            job_id: Job identifier
            files: List with single PDF file path
            options: Watermark options (type, text, opacity, rotation)

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
        watermark_type = options.get("type", "text")

        if watermark_type == "text":
            return await self._add_text_watermark(job_id, file_path, options)
        else:
            raise ValueError(f"Watermark type not supported: {watermark_type}")

    async def _add_text_watermark(
        self,
        job_id: str,
        file_path: Path,
        options: Dict[str, Any]
    ) -> str:
        """Add text watermark using frontend-generated image.

        Args:
            job_id: Job identifier
            file_path: PDF file path
            options: Watermark options (may include watermark_image base64,
                     watermark_width, watermark_height)

        Returns:
            Output file ID
        """
        # Check if frontend provided watermark image
        watermark_image_data = options.get("watermark_image")

        if not watermark_image_data:
            raise ValueError("Watermark image is required. Please ensure frontend sends watermark_image parameter.")

        # Decode base64 image
        if watermark_image_data.startswith("data:image/png;base64,"):
            watermark_image_data = watermark_image_data.split(",", 1)[1]

        image_bytes = base64.b64decode(watermark_image_data)

        # Load watermark image to get dimensions
        img = fitz.Pixmap(io.BytesIO(image_bytes))

        # 使用前端指定的水印尺寸（如果提供），否则使用图像实际尺寸
        # 这确保后端使用与前端预览相同的尺寸进行平铺
        watermark_width = options.get("watermark_width", img.width)
        watermark_height = options.get("watermark_height", img.height)
        # 水印间距（像素）
        watermark_spacing = options.get("watermark_spacing", 50)

        # Validate PDF
        doc = self.validate_pdf(file_path)
        total_pages = len(doc)

        # Create output document
        output_doc = fitz.open()

        for i in range(total_pages):
            # Update progress
            progress = int((i / total_pages) * 100)
            self.update_progress(
                job_id,
                progress,
                f"Adding watermark to page {i + 1}"
            )

            # Copy the page content
            page = doc[i]
            output_doc.insert_pdf(doc, from_page=i, to_page=i)

            # Add watermark to the copied page
            out_page = output_doc[i]
            rect = out_page.rect

            # 使用前端配置的水印尺寸和间距进行平铺
            # 计算水印单元的实际占位尺寸（包含间距）
            cell_width = watermark_width + watermark_spacing
            cell_height = watermark_height + watermark_spacing

            # 计算需要在页面放置的水印行列数
            columns = max(1, int((rect.width + watermark_spacing) / cell_width) + 1)
            rows = max(1, int((rect.height + watermark_spacing) / cell_height) + 1)

            # Tile watermark across the page with spacing
            for row in range(rows):
                for col in range(columns):
                    x = col * cell_width
                    y = row * cell_height

                    # 只在页面范围内插入水印
                    if x < rect.width and y < rect.height:
                        # 使用前端指定的尺寸插入图像
                        out_page.insert_image(
                            fitz.Rect(x, y, x + watermark_width, y + watermark_height),
                            pixmap=img,
                            overlay=True
                        )

        # Save output
        output_path = self.get_output_path(job_id, "watermarked.pdf")
        output_doc.save(output_path)
        output_doc.close()
        doc.close()

        # Complete job
        file_size = output_path.stat().st_size
        job_service.complete_job(job_id, {
            "output_file_id": job_id,
            "filename": "watermarked.pdf",
            "size": file_size,
            "pages": total_pages,
            "download_url": f"/api/v1/files/download/{job_id}",
            "expires_at": (datetime.now() + timedelta(hours=settings.FILE_EXPIRE_HOURS)).isoformat()
        })

        return job_id


@registry.register("pdf_to_images")
class PDFToImagesProcessor(BaseProcessor):
    """Processor for converting PDF to images."""

    async def process(
        self,
        job_id: str,
        files: list[Path],
        options: Dict[str, Any]
    ) -> str:
        """Convert PDF pages to images.

        Args:
            job_id: Job identifier
            files: List with single PDF file path
            options: Conversion options (format, dpi)

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
        dpi = int(options.get("dpi", 150))

        # Validate PDF
        doc = self.validate_pdf(file_path)
        total_pages = len(doc)

        # Create output directory
        output_dir = Path(settings.RESULT_DIR) / job_id
        output_dir.mkdir(parents=True, exist_ok=True)

        output_files = []

        # Convert each page
        zoom = dpi / 72  # zoom factor for DPI

        for i in range(total_pages):
            # Update progress
            progress = int((i / total_pages) * 100)
            self.update_progress(
                job_id,
                progress,
                f"Converting page {i + 1} to image"
            )

            page = doc[i]
            mat = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat)

            output_filename = f"page_{i + 1}.{output_format}"
            output_path = output_dir / output_filename
            pix.save(output_path)
            output_files.append(output_path)

        doc.close()

        # Create ZIP file with all images
        zip_filename = f"images_{output_format}.zip"
        zip_path = self.get_output_path(job_id, zip_filename)

        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in output_files:
                if file_path.exists():
                    zipf.write(file_path, file_path.name)

        # Verify ZIP was created
        if not zip_path.exists():
            raise RuntimeError(f"Failed to create ZIP file: {zip_path}")

        # Get ZIP file size
        file_size = zip_path.stat().st_size

        # Complete job with ZIP file info
        job_service.complete_job(job_id, {
            "output_file_id": job_id,
            "filename": zip_filename,
            "size": file_size,
            "file_count": len(output_files),
            "download_url": f"/api/v1/files/download/{job_id}",
            "expires_at": (datetime.now() + timedelta(hours=settings.FILE_EXPIRE_HOURS)).isoformat()
        })

        return job_id
