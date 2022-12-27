import numpy as np
import torch
import cv2
from labelManager import CLabelManager
import xml.etree.ElementTree as ET

#전체 오브젝트 대상으로 nms
def nms(list_label, list_box, list_score, list_cname,config_src):
    root = ET.parse(config_src).getroot()
    iou_thr = 0
    conf_thr = 0
    for common in root.findall("dnn_common"):
        for elem in common:
            if elem.tag == "iou_thr":
                iou_thr = int(elem.text)/100
            elif elem.tag == "conf_thr":
                conf_thr = int(elem.text)/100

    rst_nms_label = []
    rst_nms_box = []
    rst_nms_score = []
    rst_nms_cname = []

    list_rect_box = []

    for elem_box in list_box:
        xmin = elem_box[0]
        ymin = elem_box[1]
        xmax = elem_box[2]
        ymax = elem_box[3]

        list_rect_box.append([xmin, ymin, xmax - xmin, ymax - ymin])  # {xmin, ymin, 너비, 높이}
    # 노이즈 제거, 같은 물체에 대한 박스가 많은 것을 제거
    # 살아남은 bounding box의 인덱스를 반환한다.
    list_nms_idx = cv2.dnn.NMSBoxes(list_rect_box, list_score, conf_thr, iou_thr)


    if len(list_nms_idx) > 0:
        for idx in list_nms_idx.flatten():
            rst_nms_label.append(list_label[idx])
            rst_nms_box.append(list_box[idx])  # [xmin, ymin, xmax, ymax]
            rst_nms_score.append(list_score)
            rst_nms_cname.append(list_cname[idx])

    return rst_nms_label, rst_nms_cname, rst_nms_box, rst_nms_score

#개별 오브젝트 별로 nms
#(class넘버, 좌표, 점수, 클래스이름)
def object_nms(list_label, list_box, list_score, list_cname, config_src):
    root = ET.parse(config_src).getroot()
    class_category = set(list_label)
    iou_dict = {}
    conf_dict = {}

    #iou_thr, conf_thr 담기
    for class_num in class_category:
        for common in root.findall("dnn_common"):
            for elem in common:
                if elem.tag == ("iou_thr"+str(class_num)):
                    iou_dict[class_num] = int(elem.text)/100

                elif elem.tag == ("conf_thr" + str(class_num)):
                    conf_dict[class_num] = int(elem.text)/100

    rst_nms_label = []
    rst_nms_box = []
    rst_nms_score = []
    rst_nms_cname = []
    for class_num in class_category:
        list_nms_label = []
        list_nms_score = []
        list_nms_box = []
        list_nms_rect_box = []
        list_nms_cname = []

        rst_nms_label.clear()
        rst_nms_box.clear()
        rst_nms_score.clear()
        rst_nms_cname.clear()
        for idx, elem in enumerate(list_label):
            if elem == class_num:
                list_nms_label.append(list_label[idx])
                list_nms_score.append(list_score[idx])
                list_nms_box.append(list_box[idx])

                xmin = list_box[idx][0]
                ymin = list_box[idx][1]
                xmax = list_box[idx][2]
                ymax = list_box[idx][3]

                list_nms_rect_box.append([xmin, ymin, xmax - xmin, ymax - ymin])
                list_nms_cname.append(list_cname[idx])

        list_nms_idx = cv2.dnn.NMSBoxes(list_nms_rect_box, list_nms_score, conf_dict[class_num], iou_dict[class_num])


        if len(list_nms_idx) > 0:
            for idx in list_nms_idx.flatten():
                rst_nms_label.append(list_nms_label[idx])
                rst_nms_box.append(list_nms_box[idx])
                rst_nms_score.append(list_nms_score[idx])
                rst_nms_cname.append(list_nms_cname[idx])

    return rst_nms_label, rst_nms_cname, rst_nms_box, rst_nms_score


def set_nms(img, config_src):
    model_src = ""
    class_csv_src = ""
    nms_mode = 3
    root = ET.parse(config_src).getroot()
    for common in root.findall("dnn_common"):
        for elem in common:
            if elem.tag == "model_file":
                model_src = elem.text
            elif elem.tag == "class_file":
                    class_csv_src = elem.text
            elif elem.tag == "nms_mode": # nms_mode가 0이면 전체오브젝트대상 nms/ 1이면 개별 오브젝트 별로 nms
                nms_mode = int(elem.text)

    try:
        # 모델 주소
        global model
        model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_src)
    except:
        set_nms(img, config_src)


    # fromfile() : 텍스트나 이진 파일 데이터에서 배열을 생성한다.
    cv_img = np.fromfile(img, np.uint8)
    # 1D-array인 encoded_img를 3D-array로 만들어준다.
    # cv2.imread() 함수에 두 번째 파라미터로 cv2.IMREAD_COLOR를 넣어주면 BGR 방식으로 이미지를 읽습니다. cv2.IMREAD_UNCHANGED인 경우 이미지가 알파 채널을 가지고 있는 경우 BGRA 방식으로 읽습니다.
    cv_img = cv2.imdecode(cv_img, cv2.IMREAD_COLOR)
    # BGR 색상 이미지를 RGB 색상 이미지로 변환
    cv_RGB_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)

    try:
        global result
        result = model(cv_RGB_img, size=640)
    except:
        set_nms(img, config_src)
    df_result = result.pandas().xyxy[0]

    list_label = []  # 클래스번호
    list_box = []  # 좌표값
    list_score = []  # confidence값
    list_cname = []  # 클래스이름

    for idx, elem in df_result.iterrows():
        f_xmin = elem["xmin"]
        f_ymin = elem["ymin"]
        f_xmax = elem["xmax"]
        f_ymax = elem["ymax"]

        f_Pred = elem["confidence"]
        nLabel = elem["class"]  # class넘버


        cls = CLabelManager("./config/", class_csv_src)
        cls.load_class_map()
        clsName = cls.get_clas_name(nLabel)

        if clsName == "none":
            continue
        xmin = int(f_xmin)
        ymin = int(f_ymin)
        xmax = int(f_xmax)
        ymax = int(f_ymax)

        list_label.append(nLabel)  # class넘버
        list_box.append([xmin, ymin, xmax, ymax])
        list_score.append(f_Pred)  # confidence
        list_cname.append(clsName)  # class이름


    if nms_mode == 0:  # 전체
        rst_nms_label, rst_nms_cname, rst_nms_box, rst_nms_score = nms(list_label, list_box, list_score,
                                                                            list_cname, config_src)
    elif nms_mode == 1:  # object별로
        rst_nms_label, rst_nms_cname, rst_nms_box, rst_nms_score = object_nms(list_label, list_box, list_score,
                                                                                   list_cname, config_src)
    else:
        print("nms_mode = 0 or 1")
        return KeyError

    return rst_nms_label, rst_nms_cname, rst_nms_box, rst_nms_score


# if __name__ == '__main__':
#     # 이미지파일들이 있는 폴더 주소
#     src = "Z:/06. Deep Learning 데이터셋/Dataset/스마트교차로/02. 학습데이터/1차_4000장_11종/images/test"
#     config_src = "C:/Users/user/PycharmProjects/smartRoad/config/smroad_config.xml"
#
#     set_nms(src, config_src)

