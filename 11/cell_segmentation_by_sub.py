# Author: ZengHao
# CreatTime: 2022/10/21
# FileName: 02
# Description: Simple introduction of the code
import math
from xml.etree import ElementTree as ET
import cv2
import imutils
import numpy as np
import matplotlib.pyplot as plt

from image_processing import *
from divide_assessment import *
from results_filter import *

xml_path_list = ["./train-5/184/184.xml", "./train-5/1308/1308.xml", "./train-5/1310/1310.xml",
                 "./train-5/1312/1312.xml", "./train-5/1315/1315.xml"]
image_path_list = ["./train-5/184/184.jpg", "./train-5/1308/1308.jpg", "./train-5/1310/1310.jpg",
                   "./train-5/1312/1312.jpg", "./train-5/1315/1315.jpg"]


# 展示不同方法处理的灰度图
def show_cell_edge(file_path_image):
    image = cv2.imread(file_path_image, cv2.IMREAD_GRAYSCALE)
    # 使用sobel算子,要能够表示出负数,更加敏感
    sobelx = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=3)
    sobelx = cv2.convertScaleAbs(sobelx)
    sobely = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=3)
    sobely = cv2.convertScaleAbs(sobely)
    sobelxy = cv2.addWeighted(sobelx, 0.5, sobely, 0.5, 0)
    image_show(sobelxy, "1")
    # 使用scharr算子，噪音
    # scharrx = cv2.Scharr(image, cv2.CV_64F, 1, 0)
    # scharrx = cv2.convertScaleAbs(scharrx)
    # scharry = cv2.Scharr(image, cv2.CV_64F, 0, 1)
    # scharry = cv2.convertScaleAbs(scharry)
    # scharrxy = cv2.addWeighted(scharrx,0.5, scharry, 0.5, 0)
    # image_show(scharrxy, "1")
    # 使用laplacian算子
    # laplacian = cv2.Laplacian(image,cv2.CV_64F)
    # laplacian = cv2.convertScaleAbs(laplacian)
    # image_show(laplacian,"1")
    # canny边缘检测，双阈值检测
    # canny = cv2.Canny(image, 200, 250)
    # image_show(canny, "1")
    # 边缘检测，绘制图像的外接矩形
    # image = cv2.imread(file_path_image)
    # image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # # image_show(image,"2")
    # ret, thresh = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
    # contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)  # 返回轮廓本身和每条轮廓的属性
    # cv2.drawContours(image, contours, -1, (0, 0, 255), 3)
    # image_show(image, "1")

    # 或者是使用模板匹配的方法p29-30,多个样本同时画出多个
    # image = cv2.imread(file_path_image, 0)# 0表示的是灰度图
    # image = np.float32(image) # 使用滤波器需要转换成float32
    # dft = cv2.dft(image, flags = cv2.DFT_COMPLEX_OUTPUT)
    # dft_shift = np.fft.fftshift(dft) # 将0频点移动到频谱的中央
    # rows, cols = image.shape
    # crow, ccol = int(rows/2), int(cols/2)
    # 高通滤波器
    # mask = np.ones((rows,cols, 2), np.uint8)
    # mask[crow-100:crow+100, ccol-100:ccol+100] = 0 # 只有在中间位置设置成0
    #
    # fshift = dft_shift*mask
    # f_ishift = np.fft.ifftshift(fshift)
    # image_back = cv2.idft(f_ishift)
    # image_back = cv2.magnitude(image_back[:,:,0], image_back[:,:,1])
    # image_show(image_back,"1")


# 对不同阈值下的两个图像相减再进行处理
def cell_segmentation_sub_method(file_path_image):
    # 设置卷积核
    kernel = np.ones(shape=(3, 3), dtype=np.uint8)
    # 读取并展示灰度图像
    image = cv2.imread(file_path_image, 0)
    # image_show(image, "0")
    # 二值化处理并显示黑白图像
    ret_1, image_one = cv2.threshold(image, 210, 255, cv2.THRESH_BINARY_INV)
    # image_show(image_one, "1")
    # 消除图像中的空洞
    image_one = cv2.dilate(image_one, kernel, iterations=2)
    # image_show(image_one, "2")
    # 还原图像
    image_one = cv2.erode(image_one, kernel, iterations=3)
    # image_show(image_one, "3")

    ret_two, image_two = cv2.threshold(image, 86, 255, cv2.THRESH_BINARY_INV)
    # image_show(image_two, "4")
    image_two = cv2.erode(image_two, kernel, iterations=0)  # 消除小的噪声
    # image_show(image_two, "5")
    image_two = cv2.dilate(image_two, kernel, iterations=0)  # 还原图像
    # image_show(image_two, "6")
    # 图像相减
    image_three = np.array(image_one) - np.array(image_two)
    # image_show(image_three, "7")
    # 对相减后的图像进行腐蚀，消除细小的边界噪声
    image_three = cv2.erode(image_three, kernel, iterations=5)
    # image_show(image_three, "8")
    # 对腐蚀后的图像进行膨胀还原图像原本的特征
    image_three = cv2.dilate(image_three, kernel, iterations=7)
    # image_show(image_three, "9")
    # 获取图像的轮廓，参数选择RETR_CCOMP检测所有的轮廓，建立内轮廓和
    # 外轮廓两个等级关系，内轮廓中还有轮廓则内轮廓内的所有轮廓均归属于外轮廓，以此类推
    contours, hierarchy = cv2.findContours(image_three, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
    cell_image = cv2.imread(file_path_image)
    cell_image_copy = cv2.imread(file_path_image)
    # 直接显示所有轮廓的作图
    cell_image = cv2.drawContours(cell_image, contours, -1, (0, 0, 255), 3)
    # image_show(cell_image, "10")
    # 轮廓的层次结构
    # num_contour = len(contours[0])
    # print(contours)
    # print(num_contour)
    # print(hierarchy)
    # print(len(hierarchy[0]))
    # print(len(hierarchy[0][0]))

    test_object = []

    # 依据轮廓绘制边框，hierarchy[0]向量的每一个元素的四个int型变量hierarchy[0][i][0]-[0][i][3]
    # 分别表示第i个轮廓的后一个轮廓，前一个轮廓，父轮廓，内嵌轮廓的索引编号，没有的话值就是-1
    i = 0
    for item in contours:
        # 没有内嵌轮廓表明就是最内层的
        if hierarchy[0][i][3] != -1:
            x, y, w, h = cv2.boundingRect(item)
            # 剔除筛选出的特别小的无效框
            if w > 10 and h > 10:
                test_object.append({'regionX': x, 'regionY': y, 'regionWidth': w, 'regionHeight': h})
            # cell_image_copy = cv2.rectangle(cell_image_copy, (x, y), (x + w, y + h), (0, 0, 255), 3)
        i = i + 1

    # 删除重叠的框中较大的一个
    test_object = inspect(test_object)
    # 依据灰度再筛选
    test_object = grayscale_filter(file_path_image, test_object, 200, )

    for item in test_object:
        cell_image_copy = cv2.rectangle(cell_image_copy, (item["regionX"], item["regionY"]),
                                        (item["regionX"] + item['regionWidth'], item["regionY"] + item["regionHeight"]),
                                        (0, 0, 255), 3)
    image_show(cell_image_copy, "7")
    # 返回所有框的信息
    return test_object


# 测试每一个数据的影响
def test_cell_segmentation_sub_method(file_path_image, first_image_threshold, first_image_dilate_num,
                                      first_image_erode_num,
                                      second_image_threshold, second_image_erode_num, second_image_dilate_num,
                                      sub_image_erode_num, sub_image_dilate_num):
    # 设置卷积核
    kernel = np.ones(shape=(3, 3), dtype=np.uint8)
    image = cv2.imread(file_path_image, 0)
    # 二值化处理并显示黑白图像
    ret_1, image_one = cv2.threshold(image, first_image_threshold, 255, cv2.THRESH_BINARY_INV)
    # 消除图像中的空洞
    image_one = cv2.dilate(image_one, kernel, iterations=first_image_dilate_num)
    # 还原图像
    image_one = cv2.erode(image_one, kernel, iterations=first_image_erode_num)
    # 二值化获取深色部分的细胞核
    ret_two, image_two = cv2.threshold(image, second_image_threshold, 255, cv2.THRESH_BINARY_INV)
    # TODO 调整顺序看性能是否可以提升
    # 消除小的噪声
    image_two = cv2.erode(image_two, kernel, iterations=second_image_erode_num)
    # 还原图像
    image_two = cv2.dilate(image_two, kernel, iterations=second_image_dilate_num)
    # 图像相减
    image_three = np.array(image_one) - np.array(image_two)
    # 对相减后的图像进行腐蚀，消除细小的边界噪声
    image_three = cv2.erode(image_three, kernel, iterations=sub_image_erode_num)
    # 对腐蚀后的图像进行膨胀还原图像原本的特征
    image_three = cv2.dilate(image_three, kernel, iterations=sub_image_dilate_num)
    # 获取图像的轮廓，参数选择RETR_CCOMP检测所有的轮廓，建立内轮廓和
    # 外轮廓两个等级关系，内轮廓中还有轮廓则内轮廓内的所有轮廓均归属于外轮廓，以此类推
    contours, hierarchy = cv2.findContours(image_three, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)

    test_object = []

    # 依据轮廓绘制边框，hierarchy[0]向量的每一个元素的四个int型变量hierarchy[0][i][0]-[0][i][3]
    # 分别表示第i个轮廓的后一个轮廓，前一个轮廓，父轮廓，内嵌轮廓的索引编号，没有的话值就是-1
    i = 0
    for item in contours:
        # 没有内嵌轮廓表明就是最内层的
        if hierarchy[0][i][3] != -1:
            x, y, w, h = cv2.boundingRect(item)
            if w > 10 and h > 10:
                test_object.append({'regionX': x, 'regionY': y, 'regionWidth': w, 'regionHeight': h})
        i = i + 1
    # 删除重叠的框中较大的一个
    test_object = inspect(test_object)
    # 依据灰度图像筛选
    # test_object = grayscale_filter(file_path_image, test_object, 200, )
    # 返回所有框的信息
    return test_object


# 测试方法在多个图像上的性能
def test_sub_method_performance(xml_path_list, image_path_list):
    test_number = len(xml_path_list)
    for i in range(test_number):
        test_object = cell_segmentation_sub_method(image_path_list[i])
        print(contrast(xml_path_list[i], test_object))


# 函数自动选择出效果较好的情况
def series_parametric_tests(xml_path_list, image_path_list):
    file_number = len(image_path_list)
    # 获取xml文件的数据减少跳转
    all_xml_infor = get_all_xml_information(xml_path_list)

    # result = []
    # 将数据写入文件
    with open("data.txt", "a", encoding="utf-8") as f:
        # 寻找一定范围内的较好参数
        for i in range(210, 211, 2):
            for j in range(2, 3, 2):
                # 膨胀之后腐蚀的次数在膨胀次数-3到+3次的效果较好
                for k in range(max(0, j - 3), j + 3, 1):
                    print(f"{i}  {j}  {k}")
                    for l in range(85, 120, 1):
                        print(f"l is {l}")
                        for m in range(0, 8, 1):
                            for n in range(max(0, m - 2), m + 2, 1):
                                for o in range(1, 8, 2):
                                    for p in range(max(0, o - 3), o + 3, 1):
                                        # 看同一参数下不同图像的效果
                                        part_list = []
                                        for index in range(file_number):
                                            test_object = test_cell_segmentation_sub_method(image_path_list[index], i,
                                                                                            j, k, l, m, n, o, p)
                                            part_result = contrast_with_xml(all_xml_infor[index], test_object)
                                            # 根据两个比值筛选出效果较好的参数
                                            if part_result[0] < 0.5 or part_result[1] < 0.5:
                                                break
                                            else:
                                                part_list.append(part_result)
                                        if len(part_list) == file_number:
                                            # result.append({"参数": [i, j, k, l, m, n, o, p], "性能": part_list})
                                            f.write(str({"参数": [i, j, k, l, m, n, o, p], "性能": part_list}) + "\n")
                                            print("success")
    # return result




print(contrast(xml_path_list[0],cell_segmentation_sub_method(image_path_list[0])))
# show_gray_image(image_path_list[0])

# test_fit_method_performance(xml_path_list, image_path_list)
# print(series_parametric_tests(xml_path_list, image_path_list))
# with open("data.txt", 'w', encoding="utf-8") as f:
#     result = series_parametric_tests(xml_path_list, image_path_list)
#     for i in range(len(result)):
#         f.write(str(result[i])+"\n")
# series_parametric_tests(xml_path_list, image_path_list)
# series_parametrics_tests_by_fit(xml_path_list, image_path_list)
# test_sub_method_performance(xml_path_list,image_path_list)
