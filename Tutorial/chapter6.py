import cv2
import numpy as np

def stack_images(scale, img_array):
    rows = len(img_array)
    cols = len(img_array[0])
    rows_available = isinstance(img_array[0], list)
    width = img_array[0][0].shape[1]
    height = img_array[0][0].shape[0]

    if rows_available:
        for x in range(0, rows):
            for y in range(0, cols):
                if img_array[x][y].shape[:2] == img_array[0][0].shape[:2]:
                    img_array[x][y] = cv2.resize(img_array[x][y], (0,0), None, scale, scale)
                else:
                    img_array[x][y] = cv2.resize(img_array[x][y], (img_array[0][0].shape[1],img_array[x][y].shape[0]), None, scale, scale)
                if len(img_array[x][y].shape) == 2: 
                    img_array[x][y]= cv2.cvtColor(img_array[x][y], cv2.COLOR_GRAY2BGR)
            


img = cv2.imread('Resources/lena.png')
img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

img_stack = stack_images(0.5, ([img,img_gray,img], [img,img,img]))

cv2.imshow("Image Stack", img_stack)
cv2.waitKey(0)
cv2.destroyAllWindows()