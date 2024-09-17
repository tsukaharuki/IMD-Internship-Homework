import cv2
import numpy as np

def remove_white_background(image):
    #画像がRGBAでない場合は、BGRA（４チャンネル）に変換
    if image.shape[2] == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
        
    #白色の背景部分を検出するための範囲を設定
    lower_white = np.array([200,200,200,0], dtype=np.uint8)
    upper_white = np.array([255,255,255,255], dtype=np.uint8)

    #白色部分のマスクを作成
    mask = cv2.inRange(image, lower_white, upper_white)

    #アルファチャンネルを操作し白色部分を透明にする
    image[:,:,3] = cv2.bitwise_not(mask)#アルファチャンネルに反映(白を透明にする)

    return image


def blend_images(background, overlay, alpha=0.5):
    
    #背景とオーバーレイのサイズを揃える
    overlay_resized = cv2.resize(overlay, (background.shape[1],background.shape[0]))
    
    #オーバーレイ画像が4チャンネル(RGBA)の場合
    if overlay_resized.shape[2] == 4:
        #アルファチャンネルを抽出
        alpha_mask = overlay_resized[:,:,3]/255.0 #0~1の範囲に正規化
        overlay_rgb = overlay_resized[:,:,:3] #RGBチャンネル
        
        #背景とオーバーレイをアルファチャンネルを用いてブレンド
        for c in range(0, 3):
            background[:,:,c] = (1.0 - alpha_mask) * background[:,:,c] + alpha_mask * overlay_rgb[:,:,c]
    
    return background
    
    #return cv2.addWeighted(background, 1 - alpha, overlay, alpha, 0)


face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

overlay_img = cv2.imread('C:/Users/reeya/GitHubAAA/IMD-Internship-Homework/Project/Resources/overlay_img.png')

#Check reading or not img 
if overlay_img is None:
    print ("Error: overlay_image.png could not be loaded. Check the file path.")
    exit() # In case No img, finish the program

overlay_img = remove_white_background(overlay_img)

#Get img form Webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:#ret is false
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    for (x,y,w,h) in faces:
    
        resized_overlay = cv2.resize(overlay_img,(w,h))
    
    
        frame[y:y+h, x:x+w] = blend_images(frame[y:y+h, x:x+w], resized_overlay)
    
    cv2.imshow('Face Detection with Overlay', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

