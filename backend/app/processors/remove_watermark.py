"""PDF remove watermark processors.

技术思路：
1. PDF不区分"水印"和"正文"，所以需要启发式检测
2. 水印特征：大字体、透明度、旋转、居中、跨页重复
3. 多策略组合：重复检测 + 特征检测 + 区域删除
"""
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple
from datetime import datetime, timedelta
from collections import defaultdict
import fitz
from app.processors.base import BaseProcessor
from app.processors.registry import registry
from app.core.config import settings
from app.services.job_service import job_service


@registry.register("remove_watermark")
class RemoveWatermarkProcessor(BaseProcessor):
    """Processor for removing watermarks from PDF.

    使用多种策略组合检测和去除水印：
    1. 跨页面重复内容检测（最可靠）
    2. 文本特征检测（大字体、旋转）
    3. 图片特征检测（大面积、居中）
    4. 区域删除（中心区域清除）
    """

    async def process(
        self,
        job_id: str,
        files: list[Path],
        options: Dict[str, Any]
    ) -> str:
        """Remove watermark from PDF.

        Args:
            job_id: Job identifier
            files: List with single PDF file path
            options: Removal options (mode, pages, ranges)

        Returns:
            Output file ID
        """
        job_service.update_job(
            job_id,
            status="processing",
            started_at=datetime.now()
        )

        file_path = files[0]
        mode = options.get("mode", "all")

        if mode == "all":
            return await self._remove_all_pages(job_id, file_path, options)
        else:
            return await self._remove_selected_pages(job_id, file_path, options)

    def _collect_content_signatures(
        self, doc: fitz.Document
    ) -> Dict[str, List[Tuple[int, Any]]]:
        """收集所有内容的签名用于重复检测。

        Returns:
            字典，键为内容签名，值为 [(页码, 位置信息), ...]
        """
        text_signatures = defaultdict(list)
        image_signatures = defaultdict(list)

        for page_num in range(len(doc)):
            page = doc[page_num]
            page_width = page.rect.width
            page_height = page.rect.height

            # 收集文本签名
            try:
                text_dict = page.get_text("dict")
                for block in text_dict.get("blocks", []):
                    if block.get("type") == 0:  # Text block
                        for line in block.get("lines", []):
                            for span in line.get("spans", []):
                                text = span.get("text", "").strip()
                                # 过滤：只考虑有意义的水印文本
                                if len(text) >= 2 and not text.isspace():
                                    font_size = span.get("size", 0)
                                    bbox = span.get("bbox", (0, 0, 0, 0))

                                    # 归一化位置（处理微小差异）
                                    norm_x = round(bbox[0] / 20) * 20
                                    norm_y = round(bbox[1] / 20) * 20

                                    # 计算是否居中
                                    center_x = (bbox[0] + bbox[2]) / 2
                                    center_y = (bbox[1] + bbox[3]) / 2
                                    is_centered = (
                                        abs(center_x - page_width / 2) < page_width * 0.15 and
                                        abs(center_y - page_height / 2) < page_height * 0.15
                                    )

                                    # 计算是否是大字体
                                    is_large = font_size > 16

                                    # 创建签名：文本内容 + 归一化位置 + 特征
                                    signature = f"T:{text}:{norm_x}:{norm_y}:{int(is_large)}:{int(is_centered)}"
                                    text_signatures[signature].append((page_num, bbox, font_size, is_centered))
            except Exception:
                pass

            # 收集图片签名
            try:
                image_list = page.get_images(full=True)
                for img_info in image_list:
                    xref = img_info[0]
                    try:
                        areas = page.get_image_rects(xref)
                        for area in areas:
                            # 计算图片覆盖率
                            img_area = area.width * area.height
                            page_area = page_width * page_height
                            coverage = img_area / page_area if page_area > 0 else 0

                            # 计算是否居中
                            center_x = (area.x0 + area.x1) / 2
                            center_y = (area.y0 + area.y1) / 2
                            is_centered = (
                                abs(center_x - page_width / 2) < page_width * 0.15 and
                                abs(center_y - page_height / 2) < page_height * 0.15
                            )

                            # 归一化
                            norm_x = round(area.x0 / 20) * 20
                            norm_y = round(area.y0 / 20) * 20
                            norm_w = round(area.width / 20) * 20

                            # 创建签名
                            signature = f"I:{xref}:{norm_x}:{norm_y}:{norm_w}:{int(coverage > 0.1)}:{int(is_centered)}"
                            image_signatures[signature].append((page_num, area, coverage, is_centered))
                    except Exception:
                        pass
            except Exception:
                pass

        return {
            "text": dict(text_signatures),
            "images": dict(image_signatures)
        }

    def _detect_repeating_watermarks(
        self,
        signatures: Dict[str, List[Tuple[int, Any]]],
        total_pages: int
    ) -> Tuple[Set[Any], Set[Any]]:
        """检测重复的水印内容。

        Args:
            signatures: 内容签名字典
            total_pages: 总页数

        Returns:
            (要删除的文本bbox集合, 要删除的图片bbox集合)
        """
        text_to_remove = set()
        images_to_remove = set()

        # 阈值：至少出现2页或20%的页面
        threshold = max(2, int(total_pages * 0.2))

        # 检测重复文本
        for sig, occurrences in signatures.get("text", {}).items():
            if len(occurrences) >= threshold:
                # 检查是否是水印特征
                for page_num, bbox, font_size, is_centered in occurrences:
                    # 大字体或居中的重复文本很可能是水印
                    if font_size > 14 or is_centered:
                        text_to_remove.add((page_num, bbox))

        # 检测重复图片
        for sig, occurrences in signatures.get("images", {}).items():
            if len(occurrences) >= threshold:
                for page_num, area, coverage, is_centered in occurrences:
                    # 大面积或居中的重复图片很可能是水印
                    if coverage > 0.05 or is_centered:
                        images_to_remove.add((page_num, area))

        return text_to_remove, images_to_remove

    def _detect_feature_watermarks(self, page: fitz.Page, page_num: int) -> Tuple[List[Any], List[Any]]:
        """基于特征检测单页上的水印。

        检测：
        1. 大字体文本（>18pt）
        2. 旋转文本
        3. 大面积居中图片（>10%页面）
        4. 对角线分布的内容

        Returns:
            (要删除的文本bbox列表, 要删除的图片area列表)
        """
        text_to_remove = []
        images_to_remove = []

        page_width = page.rect.width
        page_height = page.rect.height
        center_x = page_width / 2
        center_y = page_height / 2

        # 检测文本水印
        try:
            text_dict = page.get_text("dict")
            for block in text_dict.get("blocks", []):
                if block.get("type") == 0:  # Text
                    for line in block.get("lines", []):
                        for span in line.get("spans", []):
                            font_size = span.get("size", 0)
                            bbox = span.get("bbox", (0, 0, 0))
                            text = span.get("text", "").strip()

                            # 特征1：大字体（很可能是水印）
                            if font_size > 18:
                                text_to_remove.append(bbox)
                                continue

                            # 特征2：居中的大文本
                            text_center_x = (bbox[0] + bbox[2]) / 2
                            text_center_y = (bbox[1] + bbox[3]) / 2
                            is_centered = (
                                abs(text_center_x - center_x) < 100 and
                                abs(text_center_y - center_y) < 100
                            )
                            if is_centered and font_size > 12 and len(text) > 3:
                                text_to_remove.append(bbox)
                                continue

                            # 特征3：对角线上的文本
                            if abs(bbox[0] - bbox[2]) < 50:  # 窄文本
                                # 检查是否在对角线附近
                                diagonal_dist = abs(
                                    (bbox[1] - page_height * bbox[0] / page_width) -
                                    (page_height - page_height * bbox[2] / page_width)
                                )
                                if diagonal_dist < 100:
                                    text_to_remove.append(bbox)
        except Exception:
            pass

        # 检测图片水印
        try:
            image_list = page.get_images(full=True)
            seen_xrefs = set()
            for img_info in image_list:
                xref = img_info[0]
                if xref in seen_xrefs:
                    continue
                seen_xrefs.add(xref)

                try:
                    areas = page.get_image_rects(xref)
                    for area in areas:
                        # 计算覆盖率
                        img_area = area.width * area.height
                        page_area = page_width * page_height
                        coverage = img_area / page_area if page_area > 0 else 0

                        # 特征1：大面积图片
                        if coverage > 0.1:
                            images_to_remove.append(area)
                            continue

                        # 特征2：居中图片
                        img_center_x = (area.x0 + area.x1) / 2
                        img_center_y = (area.y0 + area.y1) / 2
                        is_centered = (
                            abs(img_center_x - center_x) < page_width * 0.15 and
                            abs(img_center_y - center_y) < page_height * 0.15
                        )
                        if is_centered and coverage > 0.03:
                            images_to_remove.append(area)
                except Exception:
                    pass
        except Exception:
            pass

        return text_to_remove, images_to_remove

    def _remove_center_content(self, page: fitz.Page) -> List[Any]:
        """删除页面中心区域的内容（激进方案）。

        适用于：水印明确在页面中心的情况
        """
        page_width = page.rect.width
        page_height = page.rect.height

        # 定义中心区域（30%宽高的中心矩形）
        center_rect = fitz.Rect(
            page_width * 0.35,
            page_height * 0.35,
            page_width * 0.65,
            page_height * 0.65
        )

        removed = []

        # 删除中心区域的文本
        try:
            text_dict = page.get_text("dict")
            for block in text_dict.get("blocks", []):
                if block.get("type") == 0:
                    for line in block.get("lines", []):
                        for span in line.get("spans", []):
                            bbox = span.get("bbox", (0, 0, 0))
                            text_rect = fitz.Rect(bbox)
                            # 检查是否在中心区域
                            if center_rect.intersects(text_rect):
                                removed.append(bbox)
        except Exception:
            pass

        # 删除中心区域的图片
        try:
            image_list = page.get_images(full=True)
            for img_info in image_list:
                xref = img_info[0]
                try:
                    areas = page.get_image_rects(xref)
                    for area in areas:
                        if center_rect.intersects(area):
                            removed.append(area)
                except Exception:
                    pass
        except Exception:
            pass

        return removed

    def _remove_watermarks_from_page(
        self,
        page: fitz.Page,
        page_num: int,
        repeating_text: Set[Any],
        repeating_images: Set[Any],
        use_center_removal: bool = False
    ) -> int:
        """从单页删除水印。

        Args:
            page: PyMuPDF页面对象
            page_num: 页码
            repeating_text: 重复文本集合 [(page_num, bbox), ...]
            repeating_images: 重复图片集合 [(page_num, area), ...]
            use_center_removal: 是否使用中心区域删除

        Returns:
            删除的数量
        """
        removed_count = 0

        # 策略1：删除重复的文本水印
        for rp, rbbox in repeating_text:
            if rp == page_num:
                rect = fitz.Rect(rbbox)
                page.add_redact_annot(rect, fill=(1, 1, 1))
                removed_count += 1

        # 策略2：删除重复的图片水印
        for rp, rarea in repeating_images:
            if rp == page_num:
                page.add_redact_annot(rarea, fill=(1, 1, 1))
                removed_count += 1

        # 策略3：基于特征检测水印
        feature_texts, feature_images = self._detect_feature_watermarks(page, page_num)

        # 避免重复删除
        for bbox in feature_texts:
            rect = fitz.Rect(bbox)
            page.add_redact_annot(rect, fill=(1, 1, 1))
            removed_count += 1

        for area in feature_images:
            page.add_redact_annot(area, fill=(1, 1, 1))
            removed_count += 1

        # 策略4：中心区域删除（激进，可选）
        if use_center_removal:
            center_items = self._remove_center_content(page)
            for item in center_items:
                rect = fitz.Rect(item)
                page.add_redact_annot(rect, fill=(1, 1, 1))
                removed_count += 1

        # 应用所有删除操作
        if removed_count > 0:
            try:
                page.apply_redactions()
            except Exception:
                pass

        return removed_count

    async def _remove_all_pages(
        self,
        job_id: str,
        file_path: Path,
        options: Dict[str, Any]
    ) -> str:
        """Remove watermarks from all pages.

        Args:
            job_id: Job identifier
            file_path: PDF file path
            options: Removal options

        Returns:
            Output file ID
        """
        doc = self.validate_pdf(file_path)
        total_pages = len(doc)

        # 阶段1：收集所有页面的内容签名
        job_service.update_job(
            job_id,
            status="processing",
            progress=5,
            message="分析文档结构..."
        )

        signatures = self._collect_content_signatures(doc)

        # 阶段2：检测重复的水印
        job_service.update_job(
            job_id,
            progress=10,
            message="检测水印..."
        )

        repeating_text, repeating_images = self._detect_repeating_watermarks(
            signatures, total_pages
        )

        # 阶段3：逐页删除水印
        for i in range(total_pages):
            progress = int(15 + (i / total_pages) * 80)
            self.update_progress(
                job_id,
                progress,
                f"处理第 {i + 1}/{total_pages} 页"
            )

            page = doc[i]
            self._remove_watermarks_from_page(
                page, i, repeating_text, repeating_images,
                use_center_removal=False  # 设为True启用中心删除
            )

        # 保存
        self.update_progress(job_id, 95, "保存文档...")
        output_path = self.get_output_path(job_id, "cleaned.pdf")
        doc.save(output_path, garbage=4, deflate=True, clean=True)
        doc.close()

        # 完成
        file_size = output_path.stat().st_size
        job_service.complete_job(job_id, {
            "output_file_id": job_id,
            "filename": "cleaned.pdf",
            "size": file_size,
            "pages": total_pages,
            "detected_watermarks": len(repeating_text) + len(repeating_images),
            "download_url": f"/api/v1/files/download/{job_id}",
            "expires_at": (datetime.now() + timedelta(hours=settings.FILE_EXPIRE_HOURS)).isoformat()
        })

        return job_id

    async def _remove_selected_pages(
        self,
        job_id: str,
        file_path: Path,
        options: Dict[str, Any]
    ) -> str:
        """Remove watermarks from selected pages only.

        Args:
            job_id: Job identifier
            file_path: PDF file path
            options: Removal options with page selection

        Returns:
            Output file ID
        """
        doc = self.validate_pdf(file_path)
        total_pages = len(doc)

        # 获取要处理的页面
        if options.get("mode") == "range":
            ranges_str = options.get("ranges", "")
            page_indices = self._parse_ranges(ranges_str, total_pages)
        elif options.get("mode") == "every":
            every_n = int(options.get("every_n", 2))
            page_indices = [i for i in range(total_pages) if (i + 1) % every_n == 0]
        else:  # single page
            page_num = int(options.get("page", 1))
            page_indices = [page_num - 1] if 0 < page_num - 1 < total_pages else []

        if not page_indices:
            raise ValueError("没有选择有效的页面")

        # 收集签名
        job_service.update_job(job_id, status="processing", progress=5, message="分析文档...")
        signatures = self._collect_content_signatures(doc)
        repeating_text, repeating_images = self._detect_repeating_watermarks(signatures, total_pages)

        # 处理选中的页面
        processed_count = 0
        for i in range(total_pages):
            progress = int(15 + (i / total_pages) * 80)
            self.update_progress(job_id, progress, f"处理第 {i + 1}/{total_pages} 页")

            if i in page_indices:
                processed_count += 1
                page = doc[i]
                self._remove_watermarks_from_page(
                    page, i, repeating_text, repeating_images,
                    use_center_removal=False
                )

        # 保存
        self.update_progress(job_id, 95, "保存文档...")
        output_path = self.get_output_path(job_id, "cleaned.pdf")
        doc.save(output_path, garbage=4, deflate=True, clean=True)
        doc.close()

        # 完成
        file_size = output_path.stat().st_size
        job_service.complete_job(job_id, {
            "output_file_id": job_id,
            "filename": "cleaned.pdf",
            "size": file_size,
            "pages": total_pages,
            "cleaned_pages": processed_count,
            "download_url": f"/api/v1/files/download/{job_id}",
            "expires_at": (datetime.now() + timedelta(hours=settings.FILE_EXPIRE_HOURS)).isoformat()
        })

        return job_id

    def _parse_ranges(self, ranges_str: str, total_pages: int) -> list[int]:
        """Parse page ranges string into list of page indices.

        Args:
            ranges_str: Ranges string (e.g., "1-3, 5, 7-9")
            total_pages: Total number of pages

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
