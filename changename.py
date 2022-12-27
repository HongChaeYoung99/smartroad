import json
from xml.etree.ElementTree import Element, SubElement, ElementTree
import os
import cv2
from tqdm import tqdm

if __name__ == "__main__":
    path = "Y:/06. Deep Learning 데이터셋/Dataset/AI허브_차량및사람인지/Incheon"
    folder = [os.path.join(path, x) for x in os.listdir(path)]
    for fo in folder:
        # os.rename(fo, fo.replace("광주광역시_-_북구_맑음_주간_-", "Gwangju"))
        lists = [os.path.join(fo, x) for x in os.listdir(fo)]
        for list in tqdm(lists):
            os.rename(list, list.replace("인천광역시_0_부평구_맑음_야간_실외","Incheon"))
