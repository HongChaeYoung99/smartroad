import cv2
import os
import util
##################################
#비디오 프레임당 사진으로 저장하는 코드#
##################################


def imwrite(filename, img, params=None):
    try:
        ext = os.path.splitext(filename)[1]
        result, n = cv2.imencode(ext, img, params)

        if result:
            with open(filename, mode='w+b') as f:
                n.tofile(f)
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False



def saveImage():
    video_paths = "Y:/06. Deep Learning 데이터셋/Dataset/임시_래미안"

    folder_links = [os.path.join(video_paths, x) for x in os.listdir(video_paths) if os.path.isdir(os.path.join(video_paths, x))]
    for folder_link in folder_links:
        video_links = [os.path.join(folder_link, x) for x in os.listdir(folder_link) if x[-3:] == "dav"]
        for video_path in video_links:
            ########################
            image_path = "C:/Users/Minji/Documents/smart_road/images/src"
            video = cv2.VideoCapture(video_path)

            if not video.isOpened():
                print("Could not Open :", video_path)
                exit(0)

            length = int(video.get(cv2.CAP_PROP_FRAME_COUNT)) #총프레임개수
            width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
            #몇프레임당 저장할지 정하는 변수
            # fps = 50
            # fps = video.get(cv2.CAP_PROP_FPS)
            total_frame_count = video.get(cv2.CAP_PROP_FRAME_COUNT)
            fps = int(total_frame_count / 51)
            if fps == 0:
                fps = 1

            print("length :", length)
            print("width :", width)
            print("height :", height)
            print("fps :", fps)
            print("total frame count :", total_frame_count)

            #
            # try:
            #     if not os.path.exists(video_path[:-4]): #파일명이름의 폴더가 있는지 확인하고 없으면 폴더를 만든다
            #         os.makedirs(video_path[:-4])
            # except OSError:
            #     print('Error: Creating directory. ' + video_path[:-4])

            count = 0
            ###########################################################################################
            # image_path = os.path.join(image_path, os.path.basename(video_path).replace(".avi", ""))
            # util.createFolder(image_path)
            #VideoCapture의 성공 유무를 반환한다.
            while (video.isOpened()):
                ret, image = video.read() # 비디오의 한 프레임씩 읽습니다. 제대로 프레임을 읽으면 ret값이 True, 실패하면 False가 나타납니다. fram에 읽은 프레임이 나옵니다
                if (int(video.get(1)) // fps != count): #
                    count += 1
                    imwrite((os.path.join(image_path, os.path.basename(video_path).replace(".dav", ""))+"-{0}.jpg".format(count-1)).replace('/', '\\'), image)
                    rate = round(float(video.get(1)) / float(video.get(cv2.CAP_PROP_FRAME_COUNT)) * 100, 2) #현재 프레임 개수
                    print('Saved frame number : {0}/{1} [{2}%]'.format(int(video.get(1)), int(total_frame_count), rate))

                if not ret:
                    break

            video.release()


if __name__ == "__main__":
    saveImage()
