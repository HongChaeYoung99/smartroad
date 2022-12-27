import nms
import os
import cv2
import util
import xml.etree.ElementTree as ET
from labelManager import CLabelManager
import shutil

####################################################################################
#selct_object_option.xml에서 오브젝트 개수를 설정해서 그 개수 이상인 이미지만 따로 모으는 코드
#해당 클래스가 있는 이미지만 따로 모을 때도 이용 가능함.
#
####################################################################################

def select_and_copy(object_dict, option_dict, img_src, selected_img_src):
    for i in range(0, 2):
        if cls.get_clas_name(i) == "SUV/RV":
            if option_dict["SUV_RV"] > object_dict["SUV_RV"]:
                print("1")
                return 0
        else:
            if option_dict[cls.get_clas_name(i).replace("﻿","")] > object_dict[cls.get_clas_name(i).replace("﻿","")]:
                print("2")
                return 0
    # 이미지 복사
    print("3")
    shutil.copy(img_src, os.path.join(selected_img_src, os.path.basename(img_src)))
    return 0

if __name__ == '__main__':
    # 이미지 폴더 주소
    src = "C:/Users/Minji/Documents/smart_road/images/src/"
    #선택된 이미지들을 넣어둘 폴더 주소
    selected_img_src = "C:/Users/Minji/Documents/smart_road/images/selected/"
    # config xml파일의 주소
    config_src = "C:/Users/Minji/Documents/smartRoad(project)/config/select_object_option.xml" #개수 적힌 xml파일
    config_src2 = "C:/Users/Minji/Documents/smartRoad(project)/config/smart_raemian_config.xml" #모델 config파일
    root = ET.parse(config_src).getroot()

    option_dict = {}
    for elem in root:
        option_dict[elem.tag.replace("﻿","")] = int(elem.text)
    object_dict = {}
    cls = CLabelManager("./config/","ClassMapping_people.csv")  #클래스 맵핑 파일 이름 적기
    cls.load_class_map()

    img_links = [os.path.join(src, x) for x in os.listdir(src) if x[-3:] == "jpg"]

    for img in img_links:
        for i in range(0, 2):
            if cls.get_clas_name(i) == "SUV/RV":
                object_dict["SUV_RV"] = 0
            else:
                object_dict[cls.get_clas_name(i).replace("﻿", "")] = 0
        nms_label, nms_cname, nms_box, nms_score = nms.set_nms(img, config_src2)
        print(nms_cname)
        for name in nms_cname:
            if name == "SUV/RV":
                object_dict["SUV_RV"] += 1
            else:
                name = name.replace("﻿", "")
                object_dict[name] += 1
                print(object_dict[name])

        select_and_copy(object_dict, option_dict, img, selected_img_src)



