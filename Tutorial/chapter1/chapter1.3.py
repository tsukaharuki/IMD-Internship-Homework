import cv2

cap=cv2.VideoCapture(0)     #ウェブカメラの映像を取得
cap.set(3,640)  #横幅を設定。ID3は横幅設定の項目
cap.set(4,480)  #縦幅を設定。ID4は横幅設定の項目
cap.set(10,100) #明るさを設定。 ID10

while True:     #動画の画像一枚一枚に処理をする
    success,img=cap.read()
    cv2.imshow("Video",img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break