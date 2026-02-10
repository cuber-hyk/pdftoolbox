r"""PDF watermark removal using improved image processing algorithm with text protection.

改进算法：
1. 精确水印检测 - 使用渐进式容差扩展
2. 智能背景填充 - 根据周围像素自适应填充
3. 文字边缘保护 - 检测并保护文字边缘，避免影响正文
4. 双重处理 - 大面积用简单替换，边缘用智能填充

参考：
- OpenCV Inpainting: https://docs.opencv.org/3.4/df/d3d/tutorial_py_inpainting.html
- Canny Edge Detection: https://docs.opencv.org/3.4/da/d22/tutorial_py_canny.html
"""
from pathlib import Path
from typing import Any, Dict, List
from datetime import datetime, timedelta
import io
import cv2
import numpy as np
import fitz
from PIL import Image
from app.processors.base import BaseProcessor
from app.processors.registry import registry
from app.core.config import settings
from app.services.job_service import job_service


@registry.register("remove_watermark_image")
class RemoveWatermarkImageProcessor(BaseProcessor):
    """Processor for removing watermarks using improved algorithm with text protection."""

    async def process(
        self,
        job_id: str,
        files: list[Path],
        options: Dict[str, Any]
    ) -> str:
        """Remove watermark from PDF using improved algorithm."""
        job_service.update_job(
            job_id,
            status="processing",
            started_at=datetime.now()
        )

        file_path = files[0]

        watermark_color = options.get("watermark_color", [200, 200, 200])
        tolerance = options.get("tolerance", 30)
        background_color = options.get("background_color", [255, 255, 255])
        mode = options.get("mode", "all")
        dpi = options.get("dpi", 200)
        use_inpaint = options.get("use_inpaint", True)
        protect_text = options.get("protect_text", True)  # 新增：是否保护文字

        doc = self.validate_pdf(file_path)
        total_pages = len(doc)

        if mode == "all":
            page_indices = list(range(total_pages))
        elif mode == "range":
            ranges_str = options.get("ranges", "")
            page_indices = self._parse_ranges(ranges_str, total_pages)
        elif mode == "every":
            every_n = int(options.get("every_n", 2))
            page_indices = [i for i in range(total_pages) if (i + 1) % every_n == 0]
        else:
            page_num = int(options.get("page", 1))
            page_indices = [page_num - 1] if 0 < page_num - 1 < total_pages else []

        if not page_indices:
            raise ValueError("没有选择有效的页面")

        self.update_progress(job_id, 10, "渲染PDF为图片...")
        all_images = self._render_pdf_to_images(
            doc, dpi, page_indices, job_id
        )

        self.update_progress(job_id, 40, "去除水印...")
        processed_images = []
        for idx, img in enumerate(all_images):
            progress = int(40 + (idx / len(all_images)) * 35)
            self.update_progress(job_id, progress, f"处理第 {idx + 1}/{len(all_images)} 页...")

            if use_inpaint:
                processed = self._remove_watermark_smart(
                    img,
                    watermark_color,
                    tolerance,
                    background_color,
                    protect_text
                )
            else:
                processed = self._remove_watermark_simple(
                    img,
                    watermark_color,
                    tolerance,
                    background_color
                )
            processed_images.append(processed)

        self.update_progress(job_id, 80, "重建PDF...")
        output_path = self.get_output_path(job_id, "cleaned.pdf")

        if mode != "all":
            self._rebuild_pdf_with_selected_pages(
                doc, processed_images, page_indices, output_path
            )
        else:
            self._rebuild_pdf_from_images(processed_images, output_path)

        doc.close()

        file_size = output_path.stat().st_size
        job_service.complete_job(job_id, {
            "output_file_id": job_id,
            "filename": "cleaned.pdf",
            "size": file_size,
            "pages": total_pages,
            "processed_pages": len(page_indices),
            "download_url": f"/api/v1/files/download/{job_id}",
            "expires_at": (datetime.now() + timedelta(hours=settings.FILE_EXPIRE_HOURS)).isoformat()
        })

        return job_id

    def _render_pdf_to_images(
        self,
        doc: fitz.Document,
        dpi: int,
        page_indices: List[int],
        job_id: str
    ) -> List[np.ndarray]:
        """渲染PDF页面为图片列表。"""
        images = []
        total = len(page_indices)

        for idx, page_num in enumerate(page_indices):
            progress = int(10 + (idx / total) * 25)
            self.update_progress(job_id, progress, f"渲染第 {page_num + 1} 页...")

            page = doc[page_num]
            mat = fitz.Matrix(dpi / 72, dpi / 72)

            try:
                pix = page.get_pixmap(matrix=mat, alpha=False)
                img_bytes = pix.tobytes("ppm")
                img_array = cv2.imdecode(
                    np.frombuffer(img_bytes, np.uint8),
                    cv2.IMREAD_COLOR
                )

                if img_array is None:
                    img_pil = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
                    img_array = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)

                images.append(img_array)

            except Exception:
                height = int(11 * dpi)
                width = int(8.5 * dpi)
                blank_img = np.ones((height, width, 3), dtype=np.uint8) * 255
                images.append(blank_img)

        return images

    def _detect_text_edges(
        self,
        img: np.ndarray,
        threshold1: int = 50,
        threshold2: int = 150
    ) -> np.ndarray:
        """检测文字边缘。

        使用 Canny 边缘检测识别文字和图像的边缘。
        文字通常有较强的边缘特征。

        Args:
            img: OpenCV BGR 图像
            threshold1: Canny 低阈值
            threshold2: Canny 高阈值

        Returns:
            边缘 mask（255=边缘，0=非边缘）
        """
        # 转换为灰度图
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # 使用 Canny 边缘检测
        edges = cv2.Canny(gray, threshold1, threshold2)

        # 扩展边缘区域以保护边缘周围的像素
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        edges_dilated = cv2.dilate(edges, kernel, iterations=1)

        return edges_dilated

    def _create_watermark_mask(
        self,
        img: np.ndarray,
        watermark_color: List[int],
        tolerance: int
    ) -> np.ndarray:
        """创建精确的水印 mask。

        使用渐进式容差扩展策略：
        1. 首先用小容差检测精确匹配的水印
        2. 逐步扩展容差覆盖更多区域
        3. 清理噪声和小区域
        """
        r, g, b = watermark_color
        target_bgr = np.array([b, g, r], dtype=np.int16)

        # 初始容差较小，只检测精确匹配
        initial_tol = min(tolerance, 10)
        lower_bgr = np.clip(target_bgr - initial_tol, 0, 255).astype(np.uint8)
        upper_bgr = np.clip(target_bgr + initial_tol, 0, 255).astype(np.uint8)

        mask = cv2.inRange(img, lower_bgr, upper_bgr)

        # 渐进式扩展：每次增加少量容差
        max_steps = 3
        for step in range(1, max_steps + 1):
            step_tol = initial_tol + (tolerance - initial_tol) * step / max_steps
            lower = np.clip(target_bgr - step_tol, 0, 255).astype(np.uint8)
            upper = np.clip(target_bgr + step_tol, 0, 255).astype(np.uint8)
            step_mask = cv2.inRange(img, lower, upper)
            mask = cv2.bitwise_or(mask, step_mask)

        # 形态学操作清理噪声
        kernel_small = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))

        # 开运算去除小噪点
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel_small, iterations=1)

        # 闭运算填充小空洞
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel_small, iterations=2)

        # 轻微扩展以覆盖水印边缘
        kernel_medium = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        mask = cv2.dilate(mask, kernel_medium, iterations=1)

        return mask

    def _create_safe_mask(
        self,
        watermark_mask: np.ndarray,
        text_edge_mask: np.ndarray,
        min_region_size: int = 100
    ) -> np.ndarray:
        """创建安全的 mask，排除文字边缘区域。

        Args:
            watermark_mask: 水印 mask
            text_edge_mask: 文字边缘 mask
            min_region_size: 最小区域大小（像素）

        Returns:
            安全的水印 mask（排除了文字边缘）
        """
        import sys

        # 计算原始 mask 的像素数
        original_pixels = np.sum(watermark_mask > 0)

        # 排除有文字边缘的区域
        # 文字边缘区域不应该被修改
        safe_mask = watermark_mask.copy()
        safe_mask[text_edge_mask > 0] = 0

        # 计算排除后的像素数
        safe_pixels = np.sum(safe_mask > 0)
        excluded_pixels = original_pixels - safe_pixels

        if excluded_pixels > 0:
            print(f"[DEBUG] Protected {excluded_pixels} pixels with text edges", file=sys.stderr)

        # 移除太小的区域（可能是噪点）
        num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(
            safe_mask, connectivity=8
        )

        # 创建新的 mask，只保留足够大的区域
        filtered_mask = np.zeros_like(safe_mask)

        for i in range(1, num_labels):  # 跳过背景（标签0）
            area = stats[i, cv2.CC_STAT_AREA]
            if area >= min_region_size:
                filtered_mask[labels == i] = 255

        filtered_pixels = np.sum(filtered_mask > 0)
        if safe_pixels - filtered_pixels > 0:
            print(f"[DEBUG] Removed {safe_pixels - filtered_pixels} small region pixels", file=sys.stderr)

        return filtered_mask

    def _flood_fill_background(
        self,
        img: np.ndarray,
        mask: np.ndarray,
        background_color: List[int]
    ) -> np.ndarray:
        """使用背景色填充水印区域（简单快速）。"""
        result = img.copy()
        bg_r, bg_g, bg_b = background_color
        result[mask > 0] = [bg_b, bg_g, bg_r]
        return result

    def _inpaint_watermark(
        self,
        img: np.ndarray,
        mask: np.ndarray
    ) -> np.ndarray:
        """使用 inpainting 智能填充水印区域。"""
        try:
            # 使用较大的半径以获得更好的填充效果
            result = cv2.inpaint(
                img,
                mask,
                inpaintRadius=5,
                flags=cv2.INPAINT_TELEA
            )
            return result
        except Exception as e:
            import sys
            print(f"[DEBUG] Inpainting failed: {e}, using flood fill", file=sys.stderr)
            return self._flood_fill_background(img, mask, [255, 255, 255])

    def _remove_watermark_simple(
        self,
        img: np.ndarray,
        watermark_color: List[int],
        tolerance: int,
        background_color: List[int]
    ) -> np.ndarray:
        """简单模式：直接用背景色替换水印。"""
        import sys
        print(f"[DEBUG] Using simple flood fill mode", file=sys.stderr)

        mask = self._create_watermark_mask(img, watermark_color, tolerance)

        mask_pixels = np.sum(mask > 0)
        total_pixels = img.shape[0] * img.shape[1]
        print(f"[DEBUG] Mask: {mask_pixels} pixels ({100*mask_pixels/total_pixels:.2f}%)", file=sys.stderr)

        if mask_pixels == 0:
            return img.copy()

        return self._flood_fill_background(img, mask, background_color)

    def _remove_watermark_smart(
        self,
        img: np.ndarray,
        watermark_color: List[int],
        tolerance: int,
        background_color: List[int],
        protect_text: bool = True
    ) -> np.ndarray:
        """智能模式：结合简单填充和智能修复，保护文字边缘。

        策略：
        1. 创建精确的水印 mask
        2. 如果启用文字保护，检测并排除文字边缘区域
        3. 对于大面积连续区域，使用背景色填充
        4. 对于小面积和边缘区域，使用 inpainting
        """
        import sys
        print(f"[DEBUG] Using smart inpainting mode (text protection: {protect_text})", file=sys.stderr)

        # 创建水印 mask
        watermark_mask = self._create_watermark_mask(img, watermark_color, tolerance)

        mask_pixels = np.sum(watermark_mask > 0)
        total_pixels = img.shape[0] * img.shape[1]
        print(f"[DEBUG] Initial watermark mask: {mask_pixels} pixels ({100*mask_pixels/total_pixels:.2f}%)", file=sys.stderr)

        if mask_pixels == 0:
            return img.copy()

        # 文字边缘保护
        if protect_text:
            # 检测文字边缘
            text_edge_mask = self._detect_text_edges(img, threshold1=30, threshold2=100)

            edge_pixels = np.sum(text_edge_mask > 0)
            print(f"[DEBUG] Text edge mask: {edge_pixels} pixels ({100*edge_pixels/total_pixels:.2f}%)", file=sys.stderr)

            # 创建安全的 mask（排除文字边缘）
            safe_mask = self._create_safe_mask(watermark_mask, text_edge_mask, min_region_size=50)

            safe_pixels = np.sum(safe_mask > 0)
            print(f"[DEBUG] Safe mask after text protection: {safe_pixels} pixels ({100*safe_pixels/total_pixels:.2f}%)", file=sys.stderr)

            if safe_pixels == 0:
                print(f"[DEBUG] No safe regions to process, returning original", file=sys.stderr)
                return img.copy()

            working_mask = safe_mask
        else:
            working_mask = watermark_mask

        # 计算连通区域统计
        num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(
            working_mask, connectivity=8
        )

        # 如果只有一个大区域，直接用背景色填充
        if num_labels <= 2:  # 0 是背景，1 是水印
            print(f"[DEBUG] Single large region, using flood fill", file=sys.stderr)
            return self._flood_fill_background(img, working_mask, background_color)

        # 对于多个区域，使用 inpainting 智能填充
        print(f"[DEBUG] Multiple regions ({num_labels-1}), using inpainting", file=sys.stderr)
        return self._inpaint_watermark(img, working_mask)

    def _rebuild_pdf_from_images(
        self,
        images: List[np.ndarray],
        output_path: Path
    ) -> None:
        """从图片列表重建PDF。"""
        pil_images = []
        for img_array in images:
            img_rgb = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)
            pil_img = Image.fromarray(img_rgb)
            pil_images.append(pil_img)

        pil_images[0].save(
            str(output_path),
            save_all=True,
            append_images=pil_images[1:] if len(pil_images) > 1 else [],
            resolution=200.0,
            quality=95
        )

    def _rebuild_pdf_with_selected_pages(
        self,
        doc: fitz.Document,
        processed_images: List[np.ndarray],
        page_indices: List[int],
        output_path: Path
    ) -> None:
        """重建PDF，只替换指定的页面。"""
        output_doc = fitz.open()
        img_map = {page_idx: img for page_idx, img in zip(page_indices, processed_images)}

        for page_num in range(len(doc)):
            if page_num in img_map:
                img = img_map[page_num]
                img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                pil_img = Image.fromarray(img_rgb)

                img_bytes = io.BytesIO()
                pil_img.save(img_bytes, format="PNG")
                img_bytes.seek(0)

                img_doc = fitz.open(stream=img_bytes.read(), filetype="png")
                output_doc.insert_pdf(img_doc)
                img_doc.close()
            else:
                output_doc.insert_pdf(doc, from_page=page_num, to_page=page_num)

        output_doc.save(str(output_path), garbage=4, deflate=True)
        output_doc.close()

    def _parse_ranges(self, ranges_str: str, total_pages: int) -> list[int]:
        """解析页面范围字符串。"""
        indices = set()

        for part in ranges_str.split(','):
            part = part.strip()
            if not part:
                continue

            if '-' in part:
                if '--' in part:
                    start = int(part.split('--')[0]) - 1
                    indices.update(range(start, total_pages))
                else:
                    start, end = part.split('-')
                    start = int(start) - 1
                    end = int(end) - 1
                    indices.update(range(max(0, start), min(total_pages, end + 1)))
            else:
                page = int(part) - 1
                if 0 <= page < total_pages:
                    indices.add(page)

        return sorted(indices)
