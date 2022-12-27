#xml파일에서 txt파일로 변환하는 코드
import os
import util
from labelManager import CLabelManager
import xml.etree.ElementTree as ET
from tqdm import tqdm

################################################
#xml파일을 yolo에 쓸 수 있게 txt파일로 변경해주는 코드#
#################################################


#xml에서 정보 추출해서 info_dict딕셔너리에 넣기
def extract_info_from_xml(xml_file):
    #파일 열기
    f=open(xml_file,'r', encoding="UTF-8" )
    xml_text = f.read()
    #xml파일 읽을 준비
    root=ET.fromstring(xml_text)
    f.close()
    # root = ET.parse(xml_file).getroot()

    info_dict = {}
    info_dict['bboxes'] = [] #object들 넣을 곳

    for elem in root:
        if elem.tag == "filename":
            info_dict['filename'] = os.path.basename(xml_file).replace("xml", "jpg")

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
                        bbox[subsubelem.tag] = int(subsubelem.text)
                    info_dict['bboxes'].append(bbox)

    return info_dict


class_name_to_id_mapping = {'Plate': 0}

def convert_to_yolov5(info_dict, txt_src, config_name,ann):
    print_buffer = []
    cls = CLabelManager("./config/", config_name)
    cls.load_class_map()
    class_map = cls.get_clas_map()
    key_map = {v : k for k, v in class_map.items()}
    for b in info_dict["bboxes"]:
        try:
            class_id = int(key_map[b["class"]])
        except KeyError:
            print(ann)
            print("Invalid Class.")
        # if class_id == 200:
        #     print("classid 안넣어짐")
        #     break
        b_center_x = (b["xmin"] + b["xmax"]) / 2
        b_center_y = (b["ymin"] + b["ymax"]) / 2
        b_width = (b["xmax"]-b["xmin"])
        b_height = (b["ymax"]-b["ymin"])

        image_w, image_h, image_c = info_dict["image_size"]
        b_center_x /= image_w
        b_center_y /= image_h
        b_width /= image_w
        b_height /= image_h

        print_buffer.append("{} {:.3f} {:.3f} {:.3f} {:.3f}".format(class_id, b_center_x, b_center_y, b_width, b_height))

    util.createFolder(txt_src)

    if ".jpg" in info_dict["filename"]:
        save_file_name = os.path.join(txt_src, info_dict["filename"].replace('jpg', 'txt'))
    else:
        save_file_name = os.path.join(txt_src, info_dict["filename"].replace('jpg', '.txt'))

    print("\n".join(print_buffer),file = open(save_file_name, "w"))

if __name__ == '__main__':
    src = 'C:/Users/Minji/Documents/people_counting/labels'
    xml_src = os.path.join(src, "src")
    txt_src = os.path.join(src, "src2")
    config_name = "ClassMapping_people.csv"


    #annotations = xml파일 리스트
    #listdir은 딕셔너리에 있는 파일이름들을 리스트로 반환해주는 함수
    annotations = [os.path.join(xml_src, x) for x in os.listdir(xml_src) if x[-3:] == "xml"]
    # createFolder('C:/Users/user/Documents/B/labels/src3')
    annotations.sort()
    #xml파일들을 하나씩 txt로 변환
    #tqdm은 실행중인 상태를 표시해주는 상태바가 나오는 함수
    for ann in tqdm(annotations):
        info_dict = extract_info_from_xml(ann)
        convert_to_yolov5(info_dict, txt_src, config_name,ann)

    # #txt파일 리스트
    # annotations = [os.path.join('dataset/labels/src2', x) for x in os.listdir('dataset/labels/src2') if x[-3:] == "txt"]

