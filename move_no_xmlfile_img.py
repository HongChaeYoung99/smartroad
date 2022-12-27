import os
import util
import shutil
###################################
#xml파일이 없는 이미지를 골라내는 코드##
##################################
if  __name__ == "__main__":
    images_src = "C:/Users/user/Documents/smart_road/images"
    xml_src = "C:/Users/user/Documents/smart_road/labels/xml"
    noObject_src = "C:/Users/user/Documents/smart_road/noObject_images"
    img_links = [os.path.join(images_src, x) for x in os.listdir(images_src) if x[-3:] == "jpg"]
    xml_links = [os.path.join(xml_src, x) for x in os.listdir(xml_src) if x[-3:] == "xml"]
    util.createFolder(noObject_src)

    for img in img_links:
        if not os.path.isfile(os.path.join(xml_src, os.path.basename(img.replace("jpg", "xml")))):
            new_src = os.path.join(noObject_src, os.path.basename(img))
            shutil.move(img, new_src)
            print("move ", os.path.basename(img))

