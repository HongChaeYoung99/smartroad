import json
from xml.etree.ElementTree import Element, SubElement, ElementTree
import util
import os
import cv2
from tqdm import tqdm

#################################################
#json형식으로 되어있는 라벨링 파일을 xml로 바꾸는 코드##
#################################################

def isEmpty(list):
   for element in list:
     if element:
       return True
     return False
def extract_info_from_json(json_file):
    with open(json_link, "r", encoding="utf8") as f:
        contents = f.read()  # string 타입
        json_data = json.loads(contents)
    dict = {}
    dict["size"] = [json_data["camera"]["resolution_width"], json_data["camera"]["resolution_height"],3]
    dict["filename"] = os.path.basename(json_file).replace("json", "xml")
    dict["folder"] = os.path.dirname(json_file)
    dict["bboxes"] = []
    for annotation in json_data['annotations']:
        bbox = {}
        if annotation["label"] == "일반차량" or annotation["label"] == "목적차량(특장차)":
            bbox["class"] = "Car"
        elif annotation["label"] == "이륜차" and (annotation["attributes"][annotation["label"]] == "오토바이"):
            bbox["class"] = "MotorCycle"
        elif ((annotation["label"] == "보행자") and (annotation["attributes"][annotation["label"]] == "자전거" or (annotation["attributes"][annotation["label"]] == "어린이"))):
            bbox["class"] = "Bicycle"
        elif ((annotation["label"] == "보행자") and (annotation["attributes"][annotation["label"]] == "성인(노인포함)")):
            bbox["class"] = "Person"
        elif annotation["label"] == "이륜차" and (annotation["attributes"][annotation["label"]] == '전동휠/전동킥보드/전동휠체어'):
            bbox["class"] = "PM"
        bbox["xmin"] = annotation["points"][0][0]
        bbox["ymin"] = annotation["points"][0][1]
        bbox["xmax"] = annotation["points"][2][0]
        bbox["ymax"] = annotation["points"][2][1]
        dict['bboxes'].append(bbox)
    return dict

def make_xmlfile(dict):
    root = Element("annotation")
    folder = Element("folder")
    folder.text = os.path.dirname(dict["folder"])
    root.append(folder)

    filename = Element("filename")
    xml_name = dict["filename"]
    filename.text = xml_name
    root.append(filename)

    path = Element("path")
    path.text = json_link.replace("json","xml")
    root.append(path)

    size = Element("size")
    root.append(size)

    width = SubElement(size, "width")
    width.text = dict["size"][0]
    height = SubElement(size, "height")
    height.text = dict["size"][1]
    depth = SubElement(size, "depth")
    depth.text = "3"
    for bbox in dict["bboxes"]:
        object = Element("object")
        root.append(object)
        name = SubElement(object, "name")
        name.text = bbox["class"]
        bndbox = SubElement(object, "bndbox")
        xmin = SubElement(bndbox, "xmin")
        xmin.text = str(bbox["xmin"])
        ymin = SubElement(bndbox, "ymin")
        ymin.text = str(bbox["ymin"])
        xmax = SubElement(bndbox, "xmax")
        xmax.text = str(bbox["xmax"])
        ymax = SubElement(bndbox, "ymax")
        ymax.text = str(bbox["ymax"])
    util.pretty_print(root)
    tree = ElementTree(root)
    label_src = os.path.join(folder_path, "xml")
    util.createFolder(label_src)
    fileName = os.path.join(label_src, xml_name)
    tree.write(fileName, encoding='utf-8', xml_declaration=True)

if __name__ == "__main__":
    folder1_paths = "Y:/06. Deep Learning 데이터셋/Dataset/AI허브_차량및사람인지"
    # xml 저장할 폴더 위치
    folder2_paths = [os.path.join(folder1_paths, x) for x in os.listdir(folder1_paths) if os.path.isdir(os.path.join(folder1_paths, x))]
    for folder3_paths in tqdm(folder2_paths):
        folder4_path = [os.path.join(folder3_paths, x) for x in os.listdir(folder3_paths) if os.path.isdir(os.path.join(folder3_paths, x))]
        for folder_path in folder4_path:
            json_links = [os.path.join(folder_path, x) for x in os.listdir(folder_path) if x[-4:] == "json"]
            for json_link in json_links:
                dict = extract_info_from_json(json_link)
                make_xmlfile(dict)



