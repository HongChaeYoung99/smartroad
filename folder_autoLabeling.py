import nms
from xml.etree.ElementTree import Element, SubElement, ElementTree
import os
import cv2
import util

##############################################################################
#폴더 속에 여러 개의 폴더가 있고 그 폴더들 안에 이미지가 있을 경우 사용하는 오토라벨링 코드#
#src, config_src, label_src 수정해서 사용한다.                                  #
##############################################################################

def autoLabeling():
    # 이미지 폴더 주소
    src = "C:/Users/Minji/Documents/people_counting/images"

    # config xml파일의 주소
    config_src = "C:/Users/Minji/Documents/smartRoad/config/people_config.xml"

    folder_links = [os.path.join(src, x) for x in os.listdir(src) if os.path.isdir(os.path.join(src, x))]

    print(os.listdir(src) )
    for folder in folder_links:
        img_links = [os.path.join(folder, x) for x in os.listdir(folder) if x[-3:] == "jpg"]
        # 라벨링된 xml파일이 생길 폴더 주소
        label_src = os.path.join("C:/Users/Minji/Documents/people_counting/labels", os.path.basename(folder))

        # xml 코드 만들기
        for img in img_links:
            os.rename(img, img.replace(".avi", ""))
            img = img.replace(".avi", "")
            nms_label, nms_cname, nms_box, nms_score = nms.set_nms(img, config_src)

            root = Element("annotation")
            folder = Element("folder")
            folder.text = src
            root.append(folder)

            filename = Element("filename")
            filename.text = os.path.basename(img)
            root.append(filename)

            cv_img = cv2.imread(img, cv2.IMREAD_COLOR)
            h, w, c = cv_img.shape
            size = Element("size")
            root.append(size)

            width = SubElement(size, "width")
            width.text = str(w)
            height = SubElement(size, "height")
            height.text = str(h)
            depth = SubElement(size, "depth")
            depth.text = str(c)

            for i, box in enumerate(nms_box):
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
            fileName = os.path.join(label_src, os.path.basename(img).replace("jpg", "xml"))
            tree.write(fileName, encoding='utf-8', xml_declaration=True)


if __name__ == '__main__':
    autoLabeling()


