import cv2
import numpy as np

def empty(a):
    pass

def stackImages(scale, imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]

    if rowsAvailable:
        for x in range(0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape[:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), 
                    None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], 
                    (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), 
                    None, scale, scale)
                
                if len(imgArray[x][y].shape) == 2:
                    imgArray[x][y] = cv2.cvtColor(imgArray[x][y], 
                    cv2.COLOR_GRAY2BGR)
        
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), 
                None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], 
                (imgArray[0].shape[1], imgArray[0].shape[0]), 
                None, scale, scale)
            if len(imgArray[x].shape) == 2:
                imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor = np.hstack(imgArray)
        ver = hor
    return ver

path = 'Resources/mochi_moon.jpeg'
cv2.namedWindow("Moooooon")
cv2.resizeWindow("Moooooon", 320, 240)
cv2.createTrackbar("HMi", "Moooooon", 0, 179, empty)
cv2.createTrackbar("HMa", "Moooooon", 19, 179, empty)
cv2.createTrackbar("SMi", "Moooooon", 110, 255, empty)
cv2.createTrackbar("SMa", "Moooooon", 240, 255, empty)
cv2.createTrackbar("VMi", "Moooooon", 153, 255, empty)
cv2.createTrackbar("VMa", "Moooooon", 255, 255, empty)

while True:
    img = cv2.imread(path)
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h_min = cv2.getTrackbarPos("HMi", "Moooooon")
    h_max = cv2.getTrackbarPos("HMa", "Moooooon")
    s_min = cv2.getTrackbarPos("SMi", "Moooooon")
    s_max = cv2.getTrackbarPos("SMa", "Moooooon")
    v_min = cv2.getTrackbarPos("VMi", "Moooooon")
    v_max = cv2.getTrackbarPos("VMa", "Moooooon")

    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])
    mask = cv2.inRange(imgHSV, lower, upper)
    imgResult = cv2.bitwise_and(img, img, mask=mask)

    cv2.imshow("Futsu Moon", img)
    cv2.imshow("HSV Moon", imgHSV)
    cv2.imshow("Mask", mask)
    cv2.imshow("Masked Moon", imgResult)

    imgStack = stackImages(0.6, ([img, imgHSV], [mask, imgResult]))
    cv2.imshow("Stacked Moon", imgStack)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break