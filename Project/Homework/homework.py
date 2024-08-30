import cv2
import numpy as np
from ultralytics import YOLO

# YOLOv8セグメンテーションモデルの読み込み
model = YOLO("yolov8n-seg.pt")

cap = cv2.VideoCapture(0)
cap.set(3,1920)
cap.set(4,1080)
cap.set(10,100)

img_back = cv2.imread("./hiroyuki.jpg")
img_back = cv2.resize(img_back,(1920,1080))

img_bird = cv2.imread("./bird.png", cv2.IMREAD_UNCHANGED)
img_bird = cv2.resize(img_bird,(100,100))

ele_bird = cv2.imread("./elephant.png", cv2.IMREAD_UNCHANGED)
ele_bird = cv2.resize(ele_bird,(300,300))

kernel = np.ones((5,5),np.uint8)

bird = False
count = 0
elephant = False
e_count = 0
alpha = 1
while True:
    
    success,img = cap.read()
    beta = 1-alpha
    results = model(img, classes=[0],conf=0.6)
    copy_img = img_back.copy()
    segmented_image = copy_img
    segmented_image = cv2.addWeighted(src1=segmented_image, alpha=alpha, src2=img, beta=beta, gamma=0)
    
    
    if bird and count < 1200:
        segmented_image[200:300,1820-count:1920-count] = segmented_image[200:300, 1820-count:1920-count] * (1 - img_bird[:, :, 3:] / 255) + \
                      img_bird[:, :, :3] * (img_bird[:, :, 3:] / 255)
        count += 200
    elif bird:
        bird = False
        
    if elephant and e_count < 1200:
        segmented_image[550:850,1620-e_count:1920-e_count] = segmented_image[550:850, 1620-e_count:1920-e_count] * (1 - ele_bird[:, :, 3:] / 255) + \
                      ele_bird[:, :, :3] * (ele_bird[:, :, 3:] / 255)
        e_count += 200
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