###################################################################
#오토레이블링 하는 코드
#src, label_src, config_src 수정해서 사용
#이미 xml파일이 있는데 거기에 다른 모델을 사용해서 object를 추가할 때 사용한다.
###################################################################

import nms
from xml.etree.ElementTree import Element, SubElement, ElementTree
import xml.etree.ElementTree as ET
import os
import cv2
import util

def autoLabeling():

    # 이미지 폴더 경로
    src = "C:/Users/Minji/Documents/smart_road/images/src/"
    # src = "C:/Users/Minji/Documents/people_counting/images"
    # 라벨링된 xml이 추가될 경로
    label_src = "C:/Users/Minji/Documents/smart_road/labels/src/"
    # config xml파일의 경로
    config_src = "C:/Users/Minji/Documents/smartRoad(project)/config/smart_raemian_config.xml"


    img_links = [os.path.join(src, x) for x in os.listdir(src) if x[-3:] == "jpg"]


    car_num = 0 #차 개수 셀때 썼던 코드

    #xml 코드 만들기
    for img in img_links:
        fileName = os.path.join(label_src, os.path.basename(img).replace("jpg", "xml"))
        # if os.path.isfile(fileName):
        #     print("pass")
        #     continue

        os.rename(img, img.replace(".avi", ""))
        img = img.replace(".avi", "")
        nms_label, nms_cname, nms_box, nms_score = nms.set_nms(img, config_src)

        tree = ET.parse(fileName)
        root = tree.getroot()

        for i, box in enumerate(nms_box):
            if nms_cname[i] == "none":
                continue
            if nms_cname[i] == "car":
                car_num += 1
            object = Element("object")
            root.append(object)
            name = SubElement(object, "name")
            name.text = nms_cname[i]
            bndbox = SubElement(object, "bndbox")
            xmin = SubElement(bndbox, "xmin")
            xmin.text = str(box[0])
            ymin = SubElement(bndbox, "ymin")
            ymin.text = str(box[1])
            xmax = SubElement(bndbox, "xmax")
            xmax.text = str(box[2])
            ymax = SubElement(bndbox, "ymax")
            ymax.text = str(box[3])

        util.pretty_print(root)
        tree = ElementTree(root)
        util.createFolder(label_src)

        tree.write(fileName, encoding='utf-8', xml_declaration=True)
    print(car_num)

if __name__ == '__main__':
    autoLabeling()

