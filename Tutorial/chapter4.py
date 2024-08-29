import cv2
import numpy as np

img = np.zeros((512, 512, 3), np.uint8)
print(img)
img[:] = 187, 200, 208

cv2.line(img, (0, 0), (250, 350), (224, 181, 191), 2)
cv2.rectangle(img, (0, 0), (250, 350), (38, 59, 165), 2)
cv2.circle(img, (400, 50), 30, (159, 153, 149), 5)
cv2.putText(img, " Mochi Ball ", 
(300, 200), cv2.FONT_HERSHEY_COMPLEX, 
1, (43, 47, 57), 3)

cv2.imshow("IroIro", img)
cv2.waitKey(0)
