# Author: ZengHao
# CreatTime: 2022/10/21
# FileName: 01
# Description: Simple introduction of the code

# 读取和保存图片
import cv2
from xml.etree import ElementTree as ET

# 文件路径列表
image_path_list = ["./train-5/184/184.jpg", "./train-5/1308/1308.jpg", "./train-5/1310/1310.jpg",
                   "./train-5/1312/1312.jpg", "./train-5/1315/1315.jpg"]
xml_path_list = ["./train-5/184/184.xml", "./train-5/1308/1308.xml", "./train-5/1310/1310.xml",
                 "./train-5/1312/1312.xml", "./train-5/1315/1315.xml"]


# 展示指定路径的图像，设置窗口的名称
def image_show_by_path(file_path, image_name):
    image = cv2.imread(file_path)
    # 设置窗口的名称，设置成NORMAL后可以拖动改变大小
    cv2.namedWindow(image_name, cv2.WINDOW_NORMAL)
    cv2.imshow(image_name, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# 展示指定的图像
def image_show(image, image_name):
    # 创建窗口，设置窗口的名称，同时设置窗口大小可以拖动改变（..._AUTOSIZE(default)自动设置大小，..._FULLSCREEN全屏显示）
    cv2.namedWindow(image_name, cv2.WINDOW_NORMAL)
    cv2.imshow(image_name, image)
    # 等待时间0毫秒表示按下任意键终止
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# 读取指定路径的图像并将图像写入指定位置
def save_image_by_path(file_path, save_path):
    image = cv2.imread(file_path)
    retval = cv2.imwrite(save_path, image)
    # 图像写入失败给出提示
    if not retval:
        print(f"{file_path} image save to {save_path} is failed!")


# 比较xml中的长宽和通道数是否和图像相等
def compare_image_xml(file_path_xml, file_path_image):
    # 解析xml文件，形成树状结构
    tree = ET.parse(file_path_xml)
    # 获取根节点根元素
    root = tree.getroot()
    # 获取文件中的图像信息
    image_width_xml = int(root.find("size").find("width").text)
    image_height_xml = int(root.find("size").find("height").text)
    image_channel_xml = int(root.find("size").find("depth").text)
    # 读取图像信息
    image = cv2.imread(file_path_image)
    shape = image.shape
    if image_width_xml == shape[1] and image_height_xml == shape[0] and image_channel_xml == shape[2]:
        return True
    else:
        return False


# 依据xml文件统计细胞的数目
def get_cell_number_xml(file_path_xml):
    tree = ET.parse(file_path_xml)  # 解析文件
    root = tree.getroot()
    cell_number = int(root.find("objCount").text)
    return cell_number


# 根据xml文件绘制标注细胞的外接矩形
def draw_cell_rect(file_path_xml, file_path_image):
    image_name = file_path_image.split("/")[-1]
    image = cv2.imread(file_path_image)
    # 解析xml文件
    tree = ET.parse(file_path_xml)
    # 获取解析后文档的根元素
    root = tree.getroot()
    # 获取文件中所有矩形的绘制信息
    objects_infor = root.findall("object")

    for rect in objects_infor:
        x_position = int(rect.find("regionX").text)
        y_position = int(rect.find("regionY").text)
        width = int(rect.find("regionWidth").text)
        height = int(rect.find("regionHeight").text)
        # 在图像上依次绘制矩形框
        cv2.rectangle(image, (x_position, y_position), (x_position + width, y_position + height), color=(0, 0, 255),
                      thickness=3)

    image_show(image, image_name)
    return image


# 保存绘制的带外接矩形的图像
def save_draw_cell_rect(file_path_xml, file_path_image, save_path):
    image = draw_cell_rect(file_path_xml, file_path_image)
    cv2.imwrite(save_path, image)
