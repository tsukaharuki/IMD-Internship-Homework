import cv2

cap = cv2.VideoCapture(0)
cap.set(3,1920)
cap.set(4,1080)
cap.set(10,100)

while True:
    success,img = cap.read()
    cv2.imshow("Video",img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break