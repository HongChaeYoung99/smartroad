import cv2
import os
import util
#############################
#이미지를 원하는 만큼 자르는 코드#
#############################

if __name__ == "__main__":
    src = "C:/Users/Minji/Documents/smart_road/images/src"
    crop_src = "C:/Users/Minji/Documents/smart_road/images/crop_src"
    util.createFolder(crop_src)
    # folder_links = [os.path.join(src, x) for x in os.listdir(src) if os.path.isdir(os.path.join(src, x))]
    # for folder in folder_links:
    # img_links = [os.path.join(folder, x) for x in os.listdir(folder) if x[-3:] == "jpg"]
    img_links = [os.path.join(src, x) for x in os.listdir(src) if x[-3:] == "jpg"]
    for img in img_links:
        image = cv2.imread(img, cv2.IMREAD_COLOR)
        h,w,c = image.shape
        dst = image.copy()
        dst = image[0:720, 0:861]
        # dst = image[280:h, 720:w]
        cv2.imwrite(os.path.join(crop_src,os.path.basename(img)), dst)