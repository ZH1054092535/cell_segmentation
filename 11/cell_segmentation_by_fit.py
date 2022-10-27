# Author: ZengHao
# CreatTime: 2022/10/27
# FileName: cell_segmentation_by_fit
# Description: Simple introduction of the code
import cv2
import numpy as np
import math

from image_processing import *
from results_filter import *
from divide_assessment import *

xml_path_list = ["./train-5/184/184.xml", "./train-5/1308/1308.xml", "./train-5/1310/1310.xml",
                 "./train-5/1312/1312.xml", "./train-5/1315/1315.xml"]
image_path_list = ["./train-5/184/184.jpg", "./train-5/1308/1308.jpg", "./train-5/1310/1310.jpg",
                   "./train-5/1312/1312.jpg", "./train-5/1315/1315.jpg"]


# 通过对圆拟合的方法对细胞分割，并展示过程
def cell_segmentation_fit_method(file_path_image):
    kernel = np.ones(shape=(3, 3), dtype=np.uint8)
    # 读取灰度图
    image = cv2.imread(file_path_image, 0)
    image_show(image, "0")
    # 二值化处理，显示灰度图
    ret, image = cv2.threshold(image, 80, 255, cv2.THRESH_BINARY_INV)
    image_show(image, "1")
    image = cv2.erode(image, kernel, iterations=5)
    # 显示腐蚀图
    image_show(image, "2")
    # 对图像进行膨胀处理
    image = cv2.dilate(image, kernel, iterations=5)
    image_show(image, "3")
    contours, hierarchy = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    # 读入新的图像进行绘制
    cell_image = cv2.imread(file_path_image)
    cell_image_two = cv2.imread(file_path_image)
    # 绘制边框
    cell_image = cv2.drawContours(cell_image, contours, -1, (0, 0, 255), 2)
    image_show(cell_image, "4")
    # 绘制矩形
    for item in contours:
        x, y, w, h = cv2.boundingRect(item)
        cell_image_two = cv2.rectangle(cell_image_two, (x, y), (x + w, y + h), (0, 0, 255), 3)
    image_show(cell_image_two, "5")

    test_object = []
    # 拟合筛选
    cell_image_three = cv2.imread(file_path_image)
    for item in contours:
        # 外接矩形的位置和长宽
        x, y, w, h = cv2.boundingRect(item)
        # 最小外接圆的圆心和半径
        (x0, y0), radius = cv2.minEnclosingCircle(item)
        # print(radius)
        # 圆的周长
        standard_cell_len = 2 * math.pi * radius
        # 实际求得的周长
        cell_len = cv2.arcLength(item, True)
        # 设置误差限作为评判的标准
        if abs(standard_cell_len - cell_len) / standard_cell_len < 0.50:
            test_object.append({'regionX': x, 'regionY': y, 'regionWidth': w, 'regionHeight': h})
    # 删除重叠的框中较大的一个
    test_object = inspect(test_object)
    # 由于提取的部分都是灰度较低的所以不用进行灰度的筛选
    for item in test_object:
        cell_image_three = cv2.rectangle(cell_image_three, (item["regionX"], item["regionY"]),
                                         (
                                             item["regionX"] + item['regionWidth'],
                                             item["regionY"] + item["regionHeight"]),
                                         (0, 0, 255), 3)
    image_show(cell_image_three, "end")
    return test_object


# 测试拟合方法的每一个参数对结果的影响
def test_cell_segmentation_fit_method(file_path_image, first_image_threshold, first_erode_num, first_dilate_num,
                                      error_range=0.3):
    # 设置卷积核
    kernel = np.ones(shape=(3, 3), dtype=np.uint8)
    image = cv2.imread(file_path_image, 0)
    ret, image = cv2.threshold(image, first_image_threshold, 255, cv2.THRESH_BINARY_INV)
    image = cv2.erode(image, kernel, iterations=first_erode_num)
    image = cv2.dilate(image, kernel, iterations=first_dilate_num)
    contours, hierarchy = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    # 开始拟合筛选
    test_object = []
    for item in contours:
        x, y, w, h = cv2.boundingRect(item)
        (x0, y0), radius = cv2.minEnclosingCircle(item)
        standard_cell_len = 2 * math.pi * radius
        cell_len = cv2.arcLength(item, True)
        if abs(standard_cell_len - cell_len) / standard_cell_len < error_range:
            test_object.append({'regionX': x, 'regionY': y, 'regionWidth': w, 'regionHeight': h})
    # 防止框出现重叠
    # test_object = inspect(test_object)
    return test_object


# 测试拟合方法在多个图像上的性能
def test_fit_method_performance(xml_path_list, image_path_list):
    test_number = len(xml_path_list)
    for i in range(test_number):
        test_object = cell_segmentation_fit_method((image_path_list[i]))
        print(contrast(xml_path_list[i], test_object))


# 函数自动选择方法拟合较好的参数
def series_parametrics_tests_by_fit(xml_path_list, image_path_list):
    file_number = len(image_path_list)
    all_xml_infor = get_all_xml_information(xml_path_list)

    with open("fit_data.txt", 'a', encoding='utf-8') as f:
        for i in range(60, 140, 2):
            print(i)
            for j in range(1, 8, 2):
                for k in range(max(0, j - 3), j + 3, 1):
                    # 查看同一参数下不同图像的效果
                    part_list = []
                    for index in range(file_number):
                        test_object = test_cell_segmentation_fit_method(image_path_list[index], i, j, k)
                        part_result = contrast_with_xml(all_xml_infor[index], test_object)
                        if part_result[0] < 0.4 or part_result[1] < 0.10:
                            break
                        else:
                            part_list.append(part_result)
                    if len(part_list) == file_number:
                        f.write(str({"参数": [i, j, k], "性能": part_list}) + "\n")
                        f.flush()
                        print("sucess")


series_parametrics_tests_by_fit(xml_path_list, image_path_list)
