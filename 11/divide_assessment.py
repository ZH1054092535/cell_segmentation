# Author: ZengHao
# CreatTime: 2022/10/25
# FileName: divide_assessment
# Description: Simple introduction of the code
from xml.etree import ElementTree as ET


# 评估的方法是xml文件矩形框的基础上向外拓展指定像素构成的矩形作为衡量的标准
def contrast(file_path_xml, test_objects, pixel=10):
    # 解析xml文件
    tree = ET.parse(file_path_xml)
    root = tree.getroot()
    objects = root.findall('object')
    # 获取xml文件中的矩形信息
    groundtruth = []

    for obj in objects:
        x_position = int(obj.find('regionX').text)
        y_position = int(obj.find('regionY').text)
        width = int(obj.find('regionWidth').text)
        height = int(obj.find('regionHeight').text)
        # 将xml文件信息存入字典列表中
        groundtruth.append({'regionX': x_position, 'regionY': y_position, 'regionWidth': width, 'regionHeight': height})

    # 列表中算法所得字典的个数
    test_count = len(test_objects)
    # 异常检测除数不能为0, 当他是0进不了下面的循环
    if test_count == 0:
        test_count = 1
    # 标注的细胞个数
    truth_count = len(groundtruth)
    true_count = 0
    # 将测试数据和xml文件数据对比
    for obj in test_objects:
        for item in groundtruth:
            if abs(item['regionX'] - obj['regionX']) <= pixel and abs(
                    item['regionY'] - obj['regionY']) <= pixel and abs(
                item['regionWidth'] + item['regionX'] - obj['regionWidth'] - obj['regionX']) <= pixel and abs(
                item['regionHeight'] + item['regionY'] - obj['regionHeight'] - obj['regionY']) <= pixel:
                true_count += 1
                break
    # 返回查全率和查准率
    return [round(true_count / truth_count, 4), round(true_count / test_count, 4)]


def get_all_xml_information(xml_path_list):
    all_xml_infor = []
    xml_file_number = len(xml_path_list)
    # 解析每一个xml文件
    for i in range(xml_file_number):
        tree = ET.parse(xml_path_list[i])
        root = tree.getroot()
        objects = root.findall('object')
        # 获取xml的矩形信息
        groundtruth = []
        for obj in objects:
            x_position = int(obj.find('regionX').text)
            y_position = int(obj.find('regionY').text)
            width = int(obj.find('regionWidth').text)
            height = int(obj.find('regionHeight').text)
            # 将xml文件信息存入字典列表中
            groundtruth.append(
                {'regionX': x_position, 'regionY': y_position, 'regionWidth': width, 'regionHeight': height})
        all_xml_infor.append(groundtruth)
    return all_xml_infor


def contrast_with_xml(xml_objects, test_objects, pixel=10):
    # 列表中算法所得字典的个数
    test_count = len(test_objects)
    # 异常检测除数不能为0, 当他是0进不了下面的循环
    if test_count == 0:
        test_count = 1
    # xml标注的细胞个数
    truth_count = len(xml_objects)
    true_count = 0
    for obj in test_objects:
        for item in xml_objects:
            if abs(item['regionX'] - obj['regionX']) <= pixel and abs(
                    item['regionY'] - obj['regionY']) <= pixel and abs(
                item['regionWidth'] + item['regionX'] - obj['regionWidth'] - obj['regionX']) <= pixel and abs(
                item['regionHeight'] + item['regionY'] - obj['regionHeight'] - obj['regionY']) <= pixel:
                true_count += 1
                break
    return [true_count / truth_count, true_count / test_count]
