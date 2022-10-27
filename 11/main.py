# Author: ZengHao
# CreatTime: 2022/10/21
# FileName: main
# Description: Simple introduction of the code
from cell_segmentation_by_sub import *
from image_processing import *
from divide_assessment import *

# 文件路径列表
image_path_list = ["./train-5/184/184.jpg", "./train-5/1308/1308.jpg", "./train-5/1310/1310.jpg",
                   "./train-5/1312/1312.jpg", "./train-5/1315/1315.jpg"]
xml_path_list = ["./train-5/184/184.xml", "./train-5/1308/1308.xml", "./train-5/1310/1310.xml",
                 "./train-5/1312/1312.xml", "./train-5/1315/1315.xml"]


# 比较所有的xml中的长宽和通道数是否和对应图像相等
def compare_all_image_xml(file_path_xml_list, file_path_image_list):
    xml_list_len = len(file_path_xml_list)
    image_list_len = len(file_path_image_list)
    # 设置标志
    count = 0
    if xml_list_len == image_list_len:
        for i in range(xml_list_len):
            flag = compare_image_xml(file_path_xml_list[i], file_path_image_list[i])
            if not flag:
                count = count + 1
                print(f"{file_path_xml_list[i]}文件结构的长宽和通道数与{file_path_image_list[i]}的不一致！！")
        if count == 0:
            return True
    else:
        print("xml文件和图像文件数目不对等")
    return False


if __name__ == '__main__':
    flag = compare_all_image_xml(xml_path_list, image_path_list)
    if flag:
        print("所有的xml文件结构中的长宽和通道数与对应的图像相同")
    else:
        print("两者之间存在不同")
