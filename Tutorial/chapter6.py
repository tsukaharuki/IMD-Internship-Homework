import cv2
import numpy as np

def stackImages(scale, imgArray):
    print(type(imgArray[0][2]))
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]

    if rowsAvailable:
        print("aaa")
        for x in range(0, rows):
            print("x, ", x)
            for y in range(0, cols):
                print("y, ", y)
                print(type(imgArray[0][2]))
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape[:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), 
                    None, scale, scale)
                else:
                    print("bbb")
                    imgArray[x][y] = cv2.resize(imgArray[x][y], 
                    (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), 
                    None, scale, scale)
                
                print(type(imgArray[0][2]))
                print(len(imgArray[x][y].shape))
                if len(imgArray[x][y].shape) == 2:
                    print("ccc")
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

img = cv2.imread('Resources\mochi_moon.jpeg')
img = cv2.resize(img, (200, 283))
imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
imgStack = stackImages(0.5, ([img, imgGray, img], [img, img, img]))

imgHor = np.hstack((img, img))
imgVer = np.vstack((img, img))
cv2.imshow("Yoko Moon", imgHor)
cv2.imshow("Tate Moon", imgVer)
cv2.imshow("Stack Moon", imgStack)
cv2.waitKey(0)
