"""测试水印颜色检测是否正确"""
import cv2
import numpy as np


def test_color_detection():
    """测试颜色检测是否正确工作"""
    import sys

    # 测试颜色
    test_color = [200, 200, 200]  # RGB
    tolerance = 30

    # 创建测试图像 - 100x100 像素
    img = np.ones((100, 100, 3), dtype=np.uint8) * 255

    # 在中心添加一个 50x50 的水印色块
    r, g, b = test_color
    img[25:75, 25:75] = [b, g, r]  # BGR 格式

    print(f"Test color RGB: {test_color}")
    print(f"Test color BGR: {[b, g, r]}")
    print(f"Tolerance: {tolerance}")

    # 构建 mask（使用后端相同的逻辑）
    target_bgr = np.array([b, g, r], dtype=np.int16)
    lower_bgr = np.clip(target_bgr - tolerance, 0, 255).astype(np.uint8)
    upper_bgr = np.clip(target_bgr + tolerance, 0, 255).astype(np.uint8)

    print(f"Lower BGR: {lower_bgr}")
    print(f"Upper BGR: {upper_bgr}")

    mask = cv2.inRange(img, lower_bgr, upper_bgr)

    print(f"Mask pixels detected: {np.sum(mask > 0)}")
    print(f"Expected: 2500 (50x50), Got: {np.sum(mask > 0)}")

    # 扩展 mask
    for i in range(1, 4):
        lower = np.clip(target_bgr - tolerance * i, 0, 255).astype(np.uint8)
        upper = np.clip(target_bgr + tolerance * i, 0, 255).astype(np.uint8)
        mask += cv2.inRange(img, lower, upper)
        print(f"After expansion {i}: {np.sum(mask > 0)} pixels")

    # 检查中心区域的像素值
    center_pixel = img[50, 50]
    print(f"Center pixel BGR: {center_pixel}")
    print(f"Center pixel RGB: {[center_pixel[2], center_pixel[1], center_pixel[0]]}")

    # 测试该像素是否在范围内
    in_range = (
        lower_bgr[0] <= center_pixel[0] <= upper_bgr[0] and
        lower_bgr[1] <= center_pixel[1] <= upper_bgr[1] and
        lower_bgr[2] <= center_pixel[2] <= upper_bgr[2]
    )
    print(f"Center pixel in range: {in_range}")


if __name__ == "__main__":
    test_color_detection()
