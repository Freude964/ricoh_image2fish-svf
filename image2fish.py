import math
import argparse
from PIL import Image, ImageDraw
import numpy as np
import os
import glob


def fisheye(input_image_path, proj_type):
    img = Image.open(input_image_path)
    w, h = img.size[0], img.size[1]  # 原图尺寸
    img_array = np.array(img)
    img_height, img_width = img_array.shape[:2]  # 获取尺寸
    l = int(h / 2)  # 原图片是4lx2l
    fisheye_image = np.zeros((2 * l, 2 * l, 3), dtype=np.uint8)  # 鱼眼图片是2lx2l
    for u in range(2 * l):
        for v in range(2 * l):
            if (u - l) ** 2 + (v - l) ** 2 <= (l) ** 2:  # 只计算圆中心范围的
                # 从原图像的0,2l为中心
                y1 = int((2 * l / np.pi) * np.arctan2(v - l, u - l))
                if proj_type == 'equaldis':
                    x1 = int(np.sqrt((u - l) ** 2 + (v - l) ** 2))  # 等距离投影
                elif proj_type == 'equalarea':
                    x1 = int(
                        (4 * l / np.pi) * np.arcsin(np.sqrt((u - l) ** 2 + (v - l) ** 2) / (np.sqrt(2) * l)))  # 等面积投影
                else:
                    raise ValueError("投影类型必须是 'equaldis' 或 'equalarea'")

                fisheye_image[int(u), int(v), :] = img_array[x1, y1, :]
    return fisheye_image


def calculate_svf(image, threshold):
    img = Image.fromarray(image)
    gray_img = img.convert("L")  # 转灰度图
    threshold_value = int(255 * threshold)  # 阈值转到0-255
    binary_img = gray_img.point(lambda p: p > threshold_value and 255)  # 阈值比对

    # Calculate the radius of the inscribed circle
    width, height = binary_img.size
    if width != height:
        raise ValueError("Image must be a square")
    radius = width / 2

    # Create a mask for the circle
    mask = Image.new('L', (width, height), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, width, height), fill=255)

    # Calculate SVF
    binary_array = np.array(binary_img)
    mask_array = np.array(mask)
    total_pixels = np.sum(mask_array / 255)
    sky_pixels = np.sum(np.logical_and(binary_array == 255, mask_array == 255))
    svf = sky_pixels / total_pixels

    return svf, binary_img  # Returns the SVF value and the processed PIL image


def process_images(folder_path, proj_type, threshold):
    # 确保输出文件夹存在
    fisheye_folder = os.path.join(folder_path, 'fisheye')
    svf_folder = os.path.join(folder_path, 'svf')
    os.makedirs(fisheye_folder, exist_ok=True)
    os.makedirs(svf_folder, exist_ok=True)

    # 遍历当前文件夹中的所有 JPG 和 PNG 图片
    for image_path in glob.glob(folder_path + '/*.JPG') + glob.glob(folder_path + '/*.PNG'):
        # 应用鱼眼效果
        fisheye_img_array = fisheye(image_path, proj_type)
        fisheye_output_img = Image.fromarray(fisheye_img_array)
        file_extension = os.path.splitext(image_path)[1]  # 获取文件扩展名
        fisheye_output_path = os.path.join(fisheye_folder, os.path.basename(image_path).replace(file_extension,
                                                                                                '_' + proj_type + file_extension))
        fisheye_output_img.save(fisheye_output_path)

        # 计算天空可视度
        svf_value, processed_image = calculate_svf(fisheye_img_array, threshold)
        svf_str = "{:.2f}".format(svf_value)
        svf_output_path = os.path.join(svf_folder, os.path.basename(image_path).replace(file_extension,
                                                                                        '_svf' + svf_str + file_extension))
        processed_image.save(svf_output_path)

        print(f"Processed image saved as: {fisheye_output_path} and {svf_output_path}")


# 调用函数
parser = argparse.ArgumentParser(description='Process images with fisheye effect and calculate SVF.')
parser.add_argument('--projection_type', type=str, default='equalarea',
                    help='投影类型，输入equaldis or equalarea，默认等面积投影')
parser.add_argument('--threshold', type=float, default=0.55, help='用于二值化计算天空可视度的阈值，默认0.55')

# 解析命令行参数
args = parser.parse_args()
current_folder = '.'  # 当前文件夹
process_images(current_folder, args.projection_type, args.threshold)  # 你可以更换为 'equaldis'