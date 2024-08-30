import cv2

img = cv2.imread(r"Resources\lambo.png")
print(img.shape)

img_resize = cv2.resize(img, (1000, 500))
print(img_resize.shape)

img_cropped = img[0:200, 200:500]
print(img_cropped.shape)


cv2.imshow("Image", img)
cv2.imshow("Image Resize", img_resize)
cv2.imshow("Image Cropped", img_cropped)
cv2.waitKey(0)
cv2.destroyAllWindows()
