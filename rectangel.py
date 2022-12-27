import os
import xml.etree.ElementTree as ET
import cv2
import numpy as np

#############################################################
#xml에 있는 좌표를 갖고 이미지에 사각형과 라벨을 표시해서 저장하는 코드#
#############################################################

#xml에서 정보 추출해서 info_dict딕셔너리에 넣기
def extract_info_from_xml(xml_file):
    #파일 열기
    f = open(xml_file, 'r', encoding="UTF-8" )
    xml_text = f.read()
    #xml파일 읽을 준비
    root = ET.fromstring(xml_text)
    f.close()
    # root = ET.parse(xml_file).getroot()

    info_dict = {}
    info_dict['bboxes'] = [] #object들 넣을 곳

    for elem in root:
        if elem.tag == "filename":
            info_dict['filename'] = os.path.basename(xml_file).replace("xml","jpg")

        elif elem.tag == "size":
            image_size = []
            for subelem in elem:
                image_size.append(int(subelem.text))

            info_dict['image_size'] = tuple(image_size)

        elif elem.tag == "object":
            bbox = {}
            for subelem in elem:
                if subelem.tag == "name":
                    bbox["class"] = subelem.text
                elif subelem.tag == "bndbox":
                    for subsubelem in subelem:
                        bbox[subsubelem.tag] = float(subsubelem.text)
                    info_dict['bboxes'].append(bbox)

    return info_dict


if __name__ == "__main__":
    # xml 저장할 폴더 위치
    label_src = "C:/Users/user/Documents/smart_road/labels/xml" #라벨 위치
    img_src = "C:/Users/user/Documents/smart_road/images" #이미지 파일 위치
    bbox_img_src = "C:/Users/user/Documents/smart_road/bbox_image/" #좌표를 표시한 이미지를 저장할 위치
    label_links = [os.path.join(label_src, x) for x in os.listdir(label_src) if x[-3:] == "xml"]

    for label in label_links:
        image = os.path.join(img_src, os.path.basename(label).replace("xml", "jpg"))
        cvImg = np.fromfile(image, np.uint8)
        cvImg = cv2.imdecode(cvImg, cv2.IMREAD_COLOR)
        cvImg = cv2.cvtColor(cvImg, cv2.COLOR_BGR2RGB)

        info_dict = extract_info_from_xml(label)
        for bbox in info_dict["bboxes"]:
            name = bbox["class"]
            xmin = int(bbox["xmin"])
            ymin = int(bbox["ymin"])
            xmax = int(bbox["xmax"])
            ymax = int(bbox["ymax"])
            org = (xmin, ymin)
            font = cv2.FONT_HERSHEY_SIMPLEX
            fontScale = 0.5
            color = (0, 255, 0)
            thickness = 2
            cv2.rectangle(cvImg, (xmin, ymin), (xmax, ymax), (255, 0, 0), 1)
            cvImg = cv2.putText(cvImg, name, org, font, fontScale, color, thickness, cv2.LINE_AA)
            cvImg = cv2.cvtColor(cvImg, cv2.COLOR_RGB2BGR)
            cv2.imwrite(os.path.join(bbox_img_src,os.path.basename(image)), cvImg)