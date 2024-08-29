import cv2
frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture("Resources/carryout2.mp4")

while True:
    success, img = cap.read()
    img = cv2.resize(img, (frameWidth, frameHeight))
    cv2.imshow("Video!", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break