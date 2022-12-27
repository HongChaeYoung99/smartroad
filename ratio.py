import xml.etree.ElementTree as ET
import os
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import matplotlib.pyplot
import seaborn as sns

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

def A_class(annotations):
    ratio = {}
    for ann in tqdm(annotations):
        info_list = extract_info_from_xml(ann)
        for info in info_list:
            if "S" in info["class"]:
                if not "symbol" in ratio:
                    ratio["symbol"] = []
                w = int(info["xmax"]) - int(info["xmin"])
                h = int(info["ymax"]) - int(info["ymin"])
                ratio["symbol"].append(round(h / w, 2))
            elif "A1" in info["class"]:
                if not "region" in ratio:
                    ratio["region"] = []
                w = int(info["xmax"]) - int(info["xmin"])
                h = int(info["ymax"]) - int(info["ymin"])
                ratio["region"].append(round(h / w, 2))

            elif "N" in info["class"]:
                if not "number" in ratio:
                    ratio["number"] = []
                w = int(info["xmax"]) - int(info["xmin"])
                h = int(info["ymax"]) - int(info["ymin"])
                ratio["number"].append(round(h / w, 2))
    color = ["green", "red", "blue"]
    bins = []
    bins.append(np.arange(0.75, 2.6, 0.25))
    bins.append(np.arange(0.3, 1.0, 0.1))
    bins.append(np.arange(0.7, 1.6, 0.1))

    for r in ratio:
        if r == "number":
            num = 0
        elif r == "region":
            num = 1
        elif r == "symbol":
            num = 2
        counts, edges, bars = plt.hist(ratio[r], bins[num], color=color[num], label='bins=10', alpha=0.5,
                                       edgecolor='whitesmoke')
        plt.bar_label(bars)
        plt.grid()
        plt.xlabel(r)
        plt.xticks(fontsize=14)
        plt.yticks(fontsize=14)
        plt.show()
    return ratio

def B_class(annotations):
    ratio = {}
    for ann in tqdm(annotations):
        info_list = extract_info_from_xml(ann)
        for info in info_list:
            if "S" in info["class"]:
                if not "symbol" in ratio:
                    ratio["symbol"] = []
                w = int(info["xmax"]) - int(info["xmin"])
                h = int(info["ymax"]) - int(info["ymin"])
                ratio["symbol"].append(round(h / w, 2))
            elif "A1" in info["class"]:
                if not "region" in ratio:
                    ratio["region"] = []
                w = int(info["xmax"]) - int(info["xmin"])
                h = int(info["ymax"]) - int(info["ymin"])
                ratio["region"].append(round(h / w, 2))

            elif "N" in info["class"]:
                if not "number" in ratio:
                    ratio["number"] = []
                w = int(info["xmax"]) - int(info["xmin"])
                h = int(info["ymax"]) - int(info["ymin"])
                ratio["number"].append(round(h / w, 2))
    color = ["green", "blue"]
    bins = []
    bins.append(np.arange(0.5, 2.5, 0.25))
    bins.append(np.arange(0.6, 1.4, 0.1))
    for r in ratio:
        if r == "number":
            num = 0
        elif r == "symbol":
            num = 1
        counts, edges, bars = plt.hist(ratio[r], bins[num], color=color[num], label='bins=10', alpha=0.5,
                                       edgecolor='whitesmoke')
        plt.bar_label(bars)
        plt.grid()
        plt.xlabel(r)
        plt.xticks(fontsize=14)
        plt.yticks(fontsize=14)
        plt.show()
    return ratio

def C_class(annotations):
    ratio = {}
    for ann in tqdm(annotations):
        info_list = extract_info_from_xml(ann)
        for info in info_list:
            if "S" in info["class"]:
                if not "symbol" in ratio:
                    ratio["symbol"] = []
                w = int(info["xmax"]) - int(info["xmin"])
                h = int(info["ymax"]) - int(info["ymin"])
                ratio["symbol"].append(round(h / w, 2))
            elif "A1" in info["class"]:
                if not "region" in ratio:
                    ratio["region"] = []
                w = int(info["xmax"]) - int(info["xmin"])
                h = int(info["ymax"]) - int(info["ymin"])
                ratio["region"].append(round(h / w, 2))

            elif "N" in info["class"]:
                if not "number" in ratio:
                    ratio["number"] = []
                w = int(info["xmax"]) - int(info["xmin"])
                h = int(info["ymax"]) - int(info["ymin"])
                ratio["number"].append(round(h / w, 2))
    color = ["green", "blue"]
    bins = []
    bins.append(np.arange(1.2, 2.8, 0.2)) #Num
    # bins.append([0.4, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0])
    bins.append(np.arange(1.0, 1.8, 0.1)) #symbol

    for r in ratio:
        if r == "number":
            num = 0
        elif r == "symbol":
            num = 1
        counts, edges, bars = plt.hist(ratio[r], bins[num], color=color[num], label='bins=10', alpha=0.5,
                                       edgecolor='whitesmoke')
        plt.bar_label(bars)
        plt.grid()
        plt.xlabel(r)
        plt.xticks(fontsize=14)
        plt.yticks(fontsize=14)
        plt.show()
    return ratio


def C2_class(annotations):
    ratio = {}
    for ann in tqdm(annotations):
        info_list = extract_info_from_xml(ann)
        for info in info_list:
            if "S" in info["class"]:
                if not "symbol" in ratio:
                    ratio["symbol"] = []
                w = int(info["xmax"]) - int(info["xmin"])
                h = int(info["ymax"]) - int(info["ymin"])
                ratio["symbol"].append(round(h / w, 2))
            elif "A2" in info["class"]:
                if not "region" in ratio:
                    ratio["region"] = []
                w = int(info["xmax"]) - int(info["xmin"])
                h = int(info["ymax"]) - int(info["ymin"])
                ratio["region"].append(round(h / w, 2))

            elif "N" in info["class"]:
                if not "number" in ratio:
                    ratio["number"] = []
                w = int(info["xmax"]) - int(info["xmin"])
                h = int(info["ymax"]) - int(info["ymin"])
                ratio["number"].append(round(h / w, 2))
    color = ["green", "red", "blue"]
    bins = []
    bins.append(np.arange(1.0, 2.6, 0.2)) #num
    bins.append(np.arange(1.0, 2.6, 0.2)) #region
    bins.append(np.arange(0.75, 2.6, 0.25)) #symbol

    for r in ratio:
        if r == "number":
            num = 0
        elif r == "region":
            num = 1
        elif r == "symbol":
            num = 2
        counts, edges, bars = plt.hist(ratio[r], bins[num], color=color[num], label='bins=10', alpha=0.5,
                                       edgecolor='whitesmoke')
        plt.bar_label(bars)
        plt.grid()
        plt.xlabel(r)
        plt.xticks(fontsize=14)
        plt.yticks(fontsize=14)
        plt.show()
    return ratio
def D_class(annotations):
    ratio = {}
    for ann in tqdm(annotations):
        info_list = extract_info_from_xml(ann)
        for info in info_list:
            if "S" in info["class"]:
                if not "symbol" in ratio:
                    ratio["symbol"] = []
                w = int(info["xmax"]) - int(info["xmin"])
                h = int(info["ymax"]) - int(info["ymin"])
                ratio["symbol"].append(round(h / w, 2))

            elif "N" in info["class"]:
                if not "number" in ratio:
                    ratio["number"] = []
                w = int(info["xmax"]) - int(info["xmin"])
                h = int(info["ymax"]) - int(info["ymin"])
                ratio["number"].append(round(h / w, 2))
    color = ["green", "blue"]
    bins = []
    bins.append(np.arange(0, 2.9, 0.5)) #Num
    # bins.append([0.4, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0])
    bins.append(np.arange(0.8, 1.6, 0.1)) #symbol

    for r in ratio:
        if r == "number":
            num = 0
        elif r == "symbol":
            num = 1
        counts, edges, bars = plt.hist(ratio[r], bins[num], color=color[num], label='bins=10', alpha=0.5,
                                       edgecolor='whitesmoke')
        plt.bar_label(bars)
        plt.grid()
        plt.xlabel(r)
        plt.xticks(fontsize=14)
        plt.yticks(fontsize=14)
        plt.show()
    return ratio
def E_class(annotations):
    ratio = {}
    for ann in tqdm(annotations):
        info_list = extract_info_from_xml(ann)
        for info in info_list:
            if "S" in info["class"]:
                if not "symbol" in ratio:
                    ratio["symbol"] = []
                w = int(info["xmax"]) - int(info["xmin"])
                h = int(info["ymax"]) - int(info["ymin"])
                ratio["symbol"].append(round(h / w, 2))
            elif "A3" in info["class"]:
                if not "region" in ratio:
                    ratio["region"] = []
                w = int(info["xmax"]) - int(info["xmin"])
                h = int(info["ymax"]) - int(info["ymin"])
                ratio["region"].append(round(h / w, 2))

            elif "N" in info["class"]:
                if not "number" in ratio:
                    ratio["number"] = []
                w = int(info["xmax"]) - int(info["xmin"])
                h = int(info["ymax"]) - int(info["ymin"])
                ratio["number"].append(round(h / w, 2))
    color = ["green", "red", "blue"]
    bins = []
    bins.append(np.arange(0.5, 3.5, 0.25)) #num
    bins.append(np.arange(0.1, 0.9, 0.1)) #region
    bins.append(np.arange(0.5, 3.6, 0.5)) #symbol

    for r in ratio:
        if r == "number":
            num = 0
        elif r == "region":
            num = 1
        elif r == "symbol":
            num = 2
        counts, edges, bars = plt.hist(ratio[r], bins[num], color=color[num], label='bins=10', alpha=0.5,
                                       edgecolor='whitesmoke')
        plt.bar_label(bars)
        plt.grid()
        plt.xlabel(r)
        plt.xticks(fontsize=14)
        plt.yticks(fontsize=14)
        plt.show()
    return ratio

def Z_class(annotations):
    ratio = {}
    for ann in tqdm(annotations):
        info_list = extract_info_from_xml(ann)
        for info in info_list:
            if "City" in info["class"]:
                if not "city" in ratio:
                    ratio["city"] = []
                w = int(info["xmax"]) - int(info["xmin"])
                h = int(info["ymax"]) - int(info["ymin"])
                ratio["city"].append(round(h / w, 2))
            elif "Char" in info["class"]:
                if not "char" in ratio:
                    ratio["char"] = []
                w = int(info["xmax"]) - int(info["xmin"])
                h = int(info["ymax"]) - int(info["ymin"])
                ratio["char"].append(round(h / w, 2))
            elif "B" in info["class"]:
                if not "B" in ratio:
                    ratio["B"] = []
                w = int(info["xmax"]) - int(info["xmin"])
                h = int(info["ymax"]) - int(info["ymin"])
                ratio["B"].append(round(h / w, 2))
            elif "N" in info["class"]:
                if not "number" in ratio:
                    ratio["number"] = []
                w = int(info["xmax"]) - int(info["xmin"])
                h = int(info["ymax"]) - int(info["ymin"])
                ratio["number"].append(round(h / w, 2))
    color = ["green", "red", "blue", "yellow"]
    bins = []
    bins.append(np.arange(0, 10, 1)) #number
    bins.append(np.arange(0.4, 1.6, 0.2)) #city
    bins.append(np.arange(0.7, 1.6, 0.1)) #char
    bins.append(np.arange(0.2, 1.9, 0.2)) #B

    for r in ratio:
        if r == "number":
            num = 0
        elif r == "city":
            num = 1
        elif r == "char":
            num = 2
        elif r == "B":
            num = 3
        counts, edges, bars = plt.hist(ratio[r], bins[num], color=color[num], label='bins=10', alpha=0.5,
                                       edgecolor='whitesmoke')
        plt.bar_label(bars)
        plt.grid()
        plt.xlabel(r)
        plt.xticks(fontsize=14)
        plt.yticks(fontsize=14)
        plt.show()
    return ratio

if __name__ == '__main__':
    # xml_src = "C:/Users/user/Documents/C0_ratio/test"
    xml_src = "C:/Users/user/Documents/Z"
    annotations = [os.path.join(xml_src, x) for x in os.listdir(xml_src) if x[-3:] == "xml"]

    ratio = Z_class(annotations)
    for i in ratio:
        print(i, "min: ", min(ratio[i])," max: ", max(ratio[i]))
    # 숫자 0, 지역: 1, 심볼: 2

