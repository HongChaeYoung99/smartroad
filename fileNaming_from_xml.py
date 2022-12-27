#이륜차 파일이름 바꾸는 프로그램

import xml.etree.ElementTree as ET
import os
from datetime import datetime
from shutil import move
from tqdm import tqdm
import time
#비어있는 딕션너리인지 확인하는 함수
def isEmpty(dictionary):
   for element in dictionary:
     if element:
       return True
     return False
def createFolder(directory):
    try:
      #폴더가 없는가?
        if not os.path.exists(directory):
            os.mkdir(directory)
    except OSError:
        print('Error: Creating directory. ' + directory)

def change(SRC):

    #xml파일 리스트
    annotations = [os.path.join(SRC, x) for x in os.listdir(SRC) if x[-3:] == "xml"]
    order_list = [] #숫자랑 xmin담을 리스트
    info_list = [] #city, b, char 담을 리스트(num도 담기지만 쓰지않음)

    #xml파일만 있고 jpg파일은 없는 경우 실패 폴더를 만들어서 그쪽으로 옮긴다
    for i in tqdm(range(0, len(annotations)), desc="check files"):
        if not os.path.exists(annotations[i].replace("xml","jpg")):
            # print(os.path.join(SRC,"실패"))
            createFolder(os.path.join(SRC,"실패"))
            move(annotations[i], os.path.join(SRC,"실패",os.path.basename(annotations[i])) )
            del annotations[i]
            continue

    for xml_file in tqdm(annotations, desc="open xml_file"):
        #xml파일 열기
        f = open(xml_file, 'r', encoding="UTF-8")
        xml_text = f.read()
        root = ET.fromstring(xml_text)
        f.close()
        info_dict = {} #{"City":"경기", "B":"과천", "Char":"가"} 담을 딕셔너리 //Num도 담기지만 사용X
        order_dict = {} # {xmin:num} 으로 담을 딕셔너리

        for elem in root:
            if elem.tag == "object":
                for subelem in elem:
                    #네임태그이면 info_dict에 이름 담기
                    if subelem.tag == "name":
                        name = subelem.text
                        if not name == "Plate":
                            element = name.split("_") #City_서울 -> City,서울
                            info_dict[element[0]] = element[1]

        #딕셔너리가 비어있지 않으면 담기
        if isEmpty(info_dict):
            info_list.append(info_dict)

        for elem in root:
            if elem.tag == "object":
                element_name = "" #번호 넣어둘 변수
                for subelem in elem:
                    if subelem.tag == "name":
                        name = subelem.text
                        element = name.split("_")  # City_서울 -> City,서울
                        if not element[0] == "Num":
                            break
                        element_name = element[1]

                    elif subelem.tag == "bndbox":
                        for subsubelem in subelem:
                            if subsubelem.tag == "xmin":
                                order_dict[int(subsubelem.text)] = element_name #{xmin:번호}
        if isEmpty(order_dict):
            order_list.append(order_dict)


    sorted_list = []
    for dict in order_list:
        sorted_list.append(sorted(dict.items()))
    # print(sorted_list[0])
    # print(sorted_list[0][0][1],sorted_list[0][1][1], sorted_list[0][2][1], sorted_list[0][3][1])
    # print(info_list[0]["B"])
    filename_list = [] #새로운 파일 이름 담아둘 리스트
    for i in tqdm(range(0, len(sorted_list)), desc="making fileName"):
        create_time = os.path.getctime(annotations[i].replace("xml","jpg"))
        timestamp = str(create_time).replace(".", "")
        try:
            if info_list[i]["City"] == "세종":
                filename = "9-" + info_list[i]["City"] + "-" + info_list[i]["Char"] + "-" + \
                           sorted_list[i][0][1] + sorted_list[i][1][1] + sorted_list[i][2][1] + sorted_list[i][3][
                               1] + "-" + str(timestamp)
            else:
                filename = "9-" + info_list[i]["City"] + "-"+ info_list[i]["B"] + "-" + info_list[i]["Char"] + "-" + sorted_list[i][0][1]+sorted_list[i][1][1]+sorted_list[i][2][1]+sorted_list[i][3][1]+"-"+str(timestamp)
            filename_list.append(filename)
        except:
            filename = "fail" + timestamp
            filename_list.append(filename)


    for i in tqdm(range(0, len(annotations)), desc="change fileName"):
        dir, fn = os.path.split(annotations[i])
        xml_link = os.path.join(dir,filename_list[i])


        #이미 동일한 이름의 xml파일이 존재하고 본인이 그 파일이 아닐 때
        if os.path.exists(xml_link+".xml") and ((xml_link+".xml") != annotations[i]):
            os.remove(xml_link+".xml")
            move(annotations[i], xml_link+".xml")
        else:
            os.rename(annotations[i], xml_link + ".xml")

        # xml파일 열기
        xml = xml_link + ".xml"
        tree = ET.parse(xml)
        root = tree.getroot()
        #xml파일안에 filename 내용 수정
        root.find('filename').text = filename_list[i]
        tree.write(xml, encoding='UTF-8', xml_declaration=True)

        jpg_link = os.path.join(dir, filename_list[i])
        # 이미 동일한 이름의 jpg파일이 있는데 본인이 그 파일이 아닐 때
        if os.path.exists(jpg_link + ".jpg") and ((jpg_link + ".jpg") != annotations[i].replace("xml", "jpg")):
            #덮어쓰기
            os.remove(jpg_link + ".jpg") #원래있던 파일을 지우고
            move(annotations[i].replace("xml","jpg"), jpg_link + ".jpg") #옮긴다
        else:
            os.rename(annotations[i].replace("xml", "jpg"), jpg_link + ".jpg")

    #파일명 뒤에 타임스탬프 안붙이는 코드
    # for i in range(0, len(annotations)):
    #     dir, fn = os.path.split(annotations[i])
    #     xml_link = os.path.join(dir,filename_list[i])
    #     #이미 동일한 이름의 xml파일이 존재하고 본인이 그 파일이 아닐 때
    #     if os.path.exists(xml_link+".xml") and ((xml_link+".xml") != annotations[i]):
    #         for j in range(2, len(annotations)):
    #             #파일이 존재하지않거나 본인이 그 파일이름 일때
    #             if not (os.path.exists(xml_link+"-"+str(j)+".xml") and ((xml_link+"-"+str(j)+".xml") != annotations[i])):
    #                 os.rename(annotations[i], xml_link+"-"+str(j)+".xml") #파일 이름 바꾸는 함수
    #                 break
    #     else:
    #         os.rename(annotations[i], xml_link+".xml")
    #
    #     jpg_link = os.path.join(dir,filename_list[i])
    #     #이미 동일한 이름의 jpg파일이 있는데 본인이 그 파일이 아닐 때
    #     if os.path.exists(jpg_link+".jpg") and ((jpg_link+".jpg") != annotations[i].replace("xml","jpg")):
    #         for j in range(2, len(annotations)):
    #             # 파일이 존재하지않거나 본인이 그 파일이름 일때
    #             if not (os.path.exists(jpg_link+"-"+str(j)+".jpg") and ((jpg_link+"-"+str(j)+".jpg") != annotations[i].replace("xml","jpg"))):
    #                 os.rename(annotations[i].replace("xml","jpg"), jpg_link+"-"+str(j)+".jpg")
    #                 break
    #     else:
    #         os.rename(annotations[i].replace("xml","jpg"), jpg_link+".jpg")



if __name__ == '__main__':
    #xml파일과 jpg파일이 있는 폴더 주소
    name = "C:/Users/user/Documents/labeling연습/Class_Z_timestamp추가"
    change(name)



