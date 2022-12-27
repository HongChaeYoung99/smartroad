import xml.etree.ElementTree as ET
import os
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import matplotlib.pyplot
import seaborn as sns
import shutil

#xml에서 정보 추출해서 info_dict딕셔너리에 넣기
def extract_info_from_xml(xml_file):
    #파일 열기
    f=open(xml_file,'r', encoding="UTF-8" )
    xml_text = f.read()
    #xml파일 읽을 준비
    root=ET.fromstring(xml_text)
    f.close()
    # root = ET.parse(xml_file).getroot()

    info_list = [] #object들 넣을 곳

    for elem in root:
        if elem.tag == "object":
            bbox = {}
            for subelem in elem:
                if subelem.tag == "name":
                    bbox["class"] = subelem.text
                elif subelem.tag == "bndbox":
                    for subsubelem in subelem:
                        bbox[subsubelem.tag] = int(subsubelem.text)
                    info_list.append(bbox)

    return info_list

if __name__ == '__main__':
    xml_src = "Z:/06. Deep Learning 데이터셋/Dataset/LPR2.0/02. 학습데이터/5차학습_통합_bbox교정/Class_D1/labels/src/"
    img_src = "Z:/06. Deep Learning 데이터셋/Dataset/LPR2.0/02. 학습데이터/5차학습_통합_bbox교정/Class_D1/images/src/"
    result_s = "C:/Users/user/Pictures/D1/symbol/"
    # result_ch = "C:/Users/user/Pictures/Z/char/"
    # result_b = "C:/Users/user/Pictures/Z/b/"
    # result_n = "C:/Users/user/Pictures/Z/number/"
    annotations = [os.path.join(xml_src, x) for x in os.listdir(xml_src) if x[-3:] == "xml"]
    ratio = {}
    for ann in tqdm(annotations):
        info_list = extract_info_from_xml(ann)
        for info in info_list:
    #         if "City" in info["class"]:
    #             if not "city" in ratio:
    #                 ratio["city"] = []
    #             w = int(info["xmax"]) - int(info["xmin"])
    #             h = int(info["ymax"]) - int(info["ymin"])
    #             if round(h / w, 2) > 1.4:
    #                 # print("resion:", ann)
    #                 i = img_src + os.path.basename(ann).replace("xml", "jpg")
    #                 i2 = result_c + os.path.basename(ann).replace("xml", "jpg")
    #                 s = result_c + os.path.basename(ann)
    #                 shutil.copy(i, i2)
    #                 shutil.copy(ann, s)
    #         elif "Char" in info["class"]:
    #             if not "char" in ratio:
    #                 ratio["char"] = []
    #             w = int(info["xmax"]) - int(info["xmin"])
    #             h = int(info["ymax"]) - int(info["ymin"])
    #             if round(h / w, 2) < 0.8:
    #                 # print("resion:", ann)
    #                 i = img_src + os.path.basename(ann).replace("xml", "jpg")
    #                 i2 = result_ch + os.path.basename(ann).replace("xml", "jpg")
    #                 s = result_ch + os.path.basename(ann)
    #                 shutil.copy(i, i2)
    #                 shutil.copy(ann, s)
    #         elif "B" in info["class"]:
    #             if not "B" in ratio:
    #                 ratio["B"] = []
    #             w = int(info["xmax"]) - int(info["xmin"])
    #             h = int(info["ymax"]) - int(info["ymin"])
    #             if round(h / w, 2) > 1.6:
    #                 # print("resion:", ann)
    #                 i = img_src + os.path.basename(ann).replace("xml", "jpg")
    #                 i2 = result_b + os.path.basename(ann).replace("xml", "jpg")
    #                 s = result_b + os.path.basename(ann)
    #                 shutil.copy(i, i2)
    #                 shutil.copy(ann, s)
    #         elif "N" in info["class"]:
    #             if not "number" in ratio:
    #                 ratio["number"] = []
    #             w = int(info["xmax"]) - int(info["xmin"])
    #             h = int(info["ymax"]) - int(info["ymin"])
    #             if round(h / w, 2) < 1:
    #                 # print("resion:", ann)
    #                 i = img_src + os.path.basename(ann).replace("xml", "jpg")
    #                 i2 = result_n + os.path.basename(ann).replace("xml", "jpg")
    #                 s = result_n + os.path.basename(ann)
    #                 shutil.copy(i, i2)
    #                 shutil.copy(ann, s)
            if "S" in info["class"]:
                if not "symbol" in ratio:
                    ratio["symbol"] = []
                w = int(info["xmax"]) - int(info["xmin"])
                h = int(info["ymax"]) - int(info["ymin"])
                if round(h/w, 2) < 0.9:
                    # print("resion:", ann)
                    i = img_src + os.path.basename(ann).replace("xml", "jpg")
                    i2 = result_s + os.path.basename(ann).replace("xml", "jpg")
                    s = result_s + os.path.basename(ann)
                    shutil.copy(i, i2)
                    shutil.copy(ann, s)
            # elif "A3" in info["class"]:
            #     if not "region" in ratio:
            #         ratio["region"] = []
            #     w = int(info["xmax"]) - int(info["xmin"])
            #     h = int(info["ymax"]) - int(info["ymin"])
            #     if round(h/w, 2) < 0.2:
            #         # print("resion:", ann)
            #         i = img_src + os.path.basename(ann).replace("xml", "jpg")
            #         i2 = result_r + os.path.basename(ann).replace("xml", "jpg")
            #         s = result_r + os.path.basename(ann)
            #         shutil.copy(i, i2)
            #         shutil.copy(ann, s)
            #
            # elif "N" in info["class"]:
            #     if not "number" in ratio:
            #         ratio["number"] = []
            #     w = int(info["xmax"]) - int(info["xmin"])
            #     h = int(info["ymax"]) - int(info["ymin"])
            #     if  round(h/w, 2) > 3.0:
            #         # print("number:", ann)
            #         i = img_src + os.path.basename(ann).replace("xml", "jpg")
            #         i2 = result_n + os.path.basename(ann).replace("xml", "jpg")
            #         s = result_n + os.path.basename(ann)
            #         shutil.copy(i, i2)
            #         shutil.copy(ann, s)

