import xml.etree.ElementTree as ET
import os

#파일 열기
if __name__ == "__main__":
    folder = "C:/Users/Minji/Documents/extractedImage/person/labels"
    label_links = [os.path.join(folder, x) for x in os.listdir(folder) if x[-3:] == "xml"]
    for xml_file in label_links:
        tree = ET.parse(xml_file)
        root = tree.getroot()

        for elem in root:
            if elem.tag == "object":
                for subelem in elem:
                    if subelem.tag == "name":
                        if subelem.text == "Motocycle":
                            subelem.text = "MotorCycle"
                            tree.write(xml_file, encoding='UTF-8', xml_declaration=True)


# "﻿person"