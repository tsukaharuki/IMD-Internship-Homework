import cv2

cap=cv2.VideoCapture("Resources/test_videos.mp4")

while True:     #動画の画像一枚一枚に処理をする
    success,img=cap.read()
    cv2.imshow("Video",img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break