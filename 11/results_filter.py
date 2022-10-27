# Author: ZengHao
# CreatTime: 2022/10/26
# FileName: results_filter
# Description: Simple introduction of the code
import cv2
import numpy as np


# 对于重叠的矩形过滤到较大的结果，防止重复划分
def inspect(objects):
    # 设置flag属性用于代表该矩形绘制是否正确，并初始化为True
    for item in objects:
        item['flag'] = True
    for obj in objects:
        regionX = int(obj['regionX'])
        regionY = int(obj['regionY'])
        regionWidth = int(obj['regionWidth'])
        regionHeight = int(obj['regionHeight'])
        for item in objects:
            x = int(item['regionX'])
            y = int(item['regionY'])
            w = int(item['regionWidth'])
            h = int(item['regionHeight'])
            flag = True
            # 判断两矩形是否不相交
            if regionX < x < regionX + regionWidth:
                if regionY < y < regionY + regionHeight:  # 第二个矩形的左上角点在第一个矩形内部
                    flag = False
                elif regionY < y + h < regionY + regionHeight:  # 第二个矩形的左下角点在第一个矩形内部
                    flag = False
            elif regionX < x + w < regionX + regionWidth:  # 第二个矩形的右上角点在第一个矩形内部
                if regionY < y < regionY + regionHeight:
                    flag = False
                elif regionY < y + h < regionY + regionHeight:  # 第二个矩形的右下角点在第一个矩形内部
                    flag = False
            if not flag:
                # 将面积更大的矩形设置为False
                if regionWidth * regionHeight > w * h:
                    obj['flag'] = False
                else:
                    item['flag'] = False
    new_objects = []
    for Obj in objects:
        if Obj['flag']:
            new_objects.append(Obj)  # 将正确的矩形存入新列表中
    return new_objects


# 对比灰度图对筛选出的矩形进行进一步的筛选
def grayscale_filter(file_path_image, test_objects, pixel_brightness_threshold=188, area_ratio_threshold=0.33):
    img = cv2.imread(file_path_image, 0)
    for obj in test_objects:
        # 获取矩形区域构成的矩阵,获取时是先y再x（先行后列）
        temp = img[obj['regionY']:obj['regionY'] + obj['regionHeight'],
               obj['regionX']:obj['regionX'] + obj['regionWidth']]
        # 统计矩阵中非0元素的个数，大于pixel_bright的元素不为0小于的就为0。
        # 对于灰度值高（亮度越亮）的就不是要提取依据面积比的将其删除
        if np.count_nonzero(temp > pixel_brightness_threshold) / (
                obj['regionHeight'] * obj['regionWidth']) > area_ratio_threshold:
            test_objects.remove(obj)
    return test_objects
