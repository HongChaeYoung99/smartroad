import xml.etree.ElementTree as ET
import os
import shutil

#파일 열기
if __name__ == "__main__":
    #빼야하는 파일이 있는 폴더
    folder = "C:/Users/Minji/Documents/images_스마트안전감시(일부삭제)_검수완"
    #비교할 파일이 있는 폴더
    forder2 = "C:/Users/Minji/Documents/빼야하는이미지/사람"
    #이동할 링크
    moved_link = "C:/Users/Minji/Documents/빼야하는이미지/x"
    img1_links = [os.path.join(folder, x) for x in os.listdir(folder) if x[-3:] == "jpg"]
    img2_links = [[x for x in os.listdir(forder2) if x[-3:] == "jpg"]]
    for img_file in img1_links:
        img = os.path.basename(img_file)
        if str(img) in str(img2_links):
            new_src = os.path.join(moved_link, os.path.basename(img_file))
            shutil.move(img_file, new_src)
