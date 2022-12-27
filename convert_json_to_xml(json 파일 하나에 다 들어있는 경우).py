import json
from xml.etree.ElementTree import Element, SubElement, ElementTree
import util
import os
import cv2
from tqdm import tqdm

#################################################
#json형식으로 되어있는 라벨링 파일을 xml로 바꾸는 코드##
#json파일 하나에 모든 xml정보가 다 들어있는 경우(ex 영상#
#################################################


def isEmpty(list):
   for element in list:
     if element:
       return True
     return False

if  __name__ == "__main__":
    #json파일 링크
    with open("C:/Users/user/Documents/smart_road/labels/json/2021-09-08_23-21-00_wed_sunny_out_do-sa_C0053-1.json", "r", encoding="utf8") as f:
        contents = f.read()  # string 타입
        json_data = json.loads(contents)
    #xml 저장할 폴더 위치
    label_src = "C:/Users/user/Documents/smart_road/labels/xml"
    #비디오 주소
    video_src = "C:/Users/user/Documents/smart_road/video/2021-09-08_23-21-00_wed_sunny_out_do-sa_C0053-1.mp4"

    dict = {}

    for annotation in json_data['annotations']:
        if annotation.get('frame') in dict:
            dict[annotation['frame']].append([annotation['id'], annotation['bbox']])
        else:
            dict[annotation['frame']] = [[annotation['id'], annotation['bbox']]]

    for object in json_data['objects']:
        if object.get('frame') in dict:
            dict[object['frame']].append([object['id'], object['bbox']])
        else:
            dict[object['frame']] = [[object['id'], object['bbox']]]

    video = cv2.VideoCapture(video_src)
    w = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    for i in tqdm(range(0, 540)):
        if i in dict:
            root = Element("annotation")

            folder = Element("folder")
            folder.text = os.path.dirname(label_src)
            root.append(folder)

            filename = Element("filename")
            xml_name = os.path.basename(video_src).replace(".mp4", "") + "-" + str(i) + ".xml"
            filename.text = xml_name
            root.append(filename)

            path = Element("path")
            path.text = os.path.join(label_src, xml_name)
            root.append(path)

            size = Element("size")

            root.append(size)

            width = SubElement(size, "width")
            width.text = str(w)
            height = SubElement(size, "height")
            height.text = str(h)
            depth = SubElement(size, "depth")
            depth.text = "3"
            for list in dict[i]:
                object = Element("object")
                root.append(object)
                name = SubElement(object, "name")
                name.text = str(list[0])
                bndbox = SubElement(object, "bndbox")
                xmin = SubElement(bndbox, "xmin")
                xmin.text = str(list[1][0])
                ymin = SubElement(bndbox, "ymin")
                ymin.text = str(list[1][1])
                xmax = SubElement(bndbox, "xmax")
                xmax.text = str(list[1][2])
                ymax = SubElement(bndbox, "ymax")
                ymax.text = str(list[1][3])

            util.pretty_print(root)
            tree = ElementTree(root)
            util.createFolder(label_src)
            fileName = os.path.join(label_src, xml_name)
            tree.write(fileName, encoding='utf-8', xml_declaration=True)

