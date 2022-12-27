import os
import shutil

if __name__ == "__main__":
    folder = "C:/Users/Minji/Documents/smart_road/images/src"
    img_11_src = "C:/Users/Minji/Documents/smart_road/images/image_11"
    image_links = [os.path.join(folder, x) for x in os.listdir(folder) if x[-3:] == "jpg"]
    for image in image_links:
        if os.path.basename(image)[-6:-4] == "10":
            new_src = os.path.join(img_11_src, os.path.basename(image))
            shutil.move(image, new_src)