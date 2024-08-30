import cv2
import numpy as np
from ultralytics import YOLO

# YOLOv8セグメンテーションモデルの読み込み
model = YOLO("yolov8n-seg.pt")

windW = 1280
windH = 720

cap = cv2.VideoCapture(0)
cap.set(3,windW)
cap.set(4,windH)
cap.set(10,100)

img_back = cv2.imread("./hiroyuki.jpg")
img_back = cv2.resize(img_back,(windW,windH))

img_office = cv2.imread("./background.jpg")
img_office = cv2.resize(img_office,(windW,windH))

img_bird = cv2.imread("./bird.png", cv2.IMREAD_UNCHANGED)
img_bird = cv2.resize(img_bird,(int(windW/19),int(windW/19)))

ele_bird = cv2.imread("./elephant.png", cv2.IMREAD_UNCHANGED)
ele_bird = cv2.resize(ele_bird,(int(windW*3/19),int(windW*3/19)))

kernel = np.ones((5,5),np.uint8)

faceCascade = cv2.CascadeClassifier("./haarcascade_frontalface_default.xml")

kiriyuki = cv2.imread("./kiriyuki.png", cv2.IMREAD_UNCHANGED)

kiri = False
back = True
bird = False
count = 0
elephant = False
e_count = 0
alpha = 1
while True:
    
    success,img = cap.read()
    beta = 1-alpha
    
    if kiri:
        imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(imgGray,1.1,4)
    
    
    results = model(img, classes=[0],conf=0.6)
    
    if back is not True:
        copy_img = img_back.copy()
        obj_max = (windW*12/19)
        kiri = True
    else:
        copy_img = img_office.copy()
        obj_max = windW - int(windW*3/19)
        kiri = False
    
    segmented_image = copy_img
    segmented_image = cv2.addWeighted(src1=segmented_image, alpha=alpha, src2=img, beta=beta, gamma=0)
    
    
    if bird and count < obj_max:
        segmented_image[int(windH/5):int(windH/5)+int(windW/19),int(windW)-int(windW/19)-count:int(windW)-count] = segmented_image[int(windH/5):int(windH/5)+int(windW/19),int(windW)-int(windW/19)-count:int(windW)-count] * (1 - img_bird[:, :, 3:] / 255) + \
                      img_bird[:, :, :3] * (img_bird[:, :, 3:] / 255)
        count += 20
    elif bird:
        bird = False
        
    if elephant and e_count < obj_max:
        segmented_image[int(windH/2):int(windH/2)+int(windW*3/19),int(windW)-int(windW*3/19)-e_count:int(windW)-e_count] = segmented_image[int(windH/2):int(windH/2)+int(windW*3/19),int(windW)-int(windW*3/19)-e_count:int(windW)-e_count]  * (1 - ele_bird[:, :, 3:] / 255) + \
                      ele_bird[:, :, :3] * (ele_bird[:, :, 3:] / 255)
        e_count += 20
    elif elephant:
        elephant = False
    
    try:
        masks = results[0].masks.data
        
        # マスクが複数ある場合を考慮して、各マスクを処理
        for mask in masks:
            mask = mask.cpu().numpy()  # マスクをNumPy配列に変換
            mask = mask.squeeze()  # 不要な次元を削除
            
            # マスクのサイズを元画像のサイズにリサイズ
            mask = cv2.resize(mask, (img.shape[1], img.shape[0]), interpolation=cv2.INTER_NEAREST)
            
            mask = mask.astype(bool)  # マスクをブール型に変換
            segmented_image[mask] = img[mask]
        
        if kiri:
            for(x,y,w,h)in faces:
                kiriyuki = cv2.resize(kiriyuki, (w, h), interpolation=cv2.INTER_LANCZOS4)
                segmented_image[y:y+h,x:x+w] = segmented_image[y:y+h,x:x+w]  * (1 - kiriyuki[:, :, 3:] / 255) + \
                        kiriyuki[:, :, :3] * (kiriyuki[:, :, 3:] / 255)
        
        cv2.imshow("Video",segmented_image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        elif cv2.waitKey(1) & 0xFF == ord('b'):
            bird = True
            count = 0
        elif cv2.waitKey(1) & 0xFF == ord('e'):
            elephant = True
            e_count = 0
        elif cv2.waitKey(1) & 0xFF == ord('i'):
            if alpha < 1:
                alpha += 0.1
            if alpha > 1:
                alpha = 1
        elif cv2.waitKey(1) & 0xFF == ord('o'):
            print(alpha)
            if alpha > 0:
                alpha -= 0.1
            if alpha < 0:
                alpha = 0
        elif cv2.waitKey(1) & 0xFF == ord('c'):
            if back == True:
                back = False
            else:
                back = True
            
                
    except:
        
        cv2.imshow("Video",segmented_image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        elif cv2.waitKey(1) & 0xFF == ord('b'):
            print("pressed")
            bird = True
            count = 0
        elif cv2.waitKey(1) & 0xFF == ord('e'):
            elephant = True
            e_count = 0
        elif cv2.waitKey(1) & 0xFF == ord('i'):
            if alpha < 1:
                alpha += 0.1
            if alpha > 1:
                alpha = 1
        elif cv2.waitKey(1) & 0xFF == ord('o'):
            if alpha > 0:
                alpha -= 0.1
            if alpha < 0:
                alpha = 0
        elif cv2.waitKey(1) & 0xFF == ord('c'):
            if back == True:
                back = False
            else:
                back = True