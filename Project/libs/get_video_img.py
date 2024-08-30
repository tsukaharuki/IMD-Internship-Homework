import cv2
import os

#ベース画像分割関数
def split_pic(img, org_cx, org_cy, splitx, splity, height, width):
    cx, cy = org_cx, org_cy
    pic_list=[]
    for j in range(splitx):
        for i in range(splity):
            spic=img[cy:cy+int(height/splity),cx:cx+int(width/splitx),:]
            pic_list.append(spic)
            cy+=int(height/splity)
        cy=org_cy
        cx+=int(width/splitx)
    #pic_list=np.array(pic_list)
    return pic_list


# ビデオから、画像を取得
def get_video_img(img_save_path):
    import cv2

    face_cascade = cv2.CascadeClassifier(r"haarcascade_frontalface_default.xml")

    #画像読み込み
    cap = cv2.VideoCapture(0)

    # カメラの映像取得
    while True:
        success, img = cap.read()
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces =face_cascade.detectMultiScale(img_gray, 1.1, 4)

        for (x,y,w,h) in faces:
            cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 1)
        cv2.imshow("Result", img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.imwrite(img_save_path, img)
            cv2.destroyAllWindows()
            break

    return faces