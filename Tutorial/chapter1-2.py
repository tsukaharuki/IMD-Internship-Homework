import cv2

cap = cv2.VideoCapture("Resources/test_video.mp4")

while True:
    success, img = cap.read()
    cv2.imshow("Video", img)
    #Getting out of the loop by 'q' 
    if cv2.waqitKey(1) & 0xFF ==ord('q'):
        break