import cv2

# ========================== read img =====================
img = cv2.imread(r"Resources\lena.png")

cv2.imshow("output", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
# =========================================================

# ========================== read video =====================
import cv2

cap = cv2.VideoCapture(r"Resources\test_video.mp4")
while True:
    success, img = cap.read()
    if not success:
        break
    cv2.imshow("Result", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# ============================================================

# ========================== read webcam =====================
cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)

while True:
    success, img = cap.read()

    cv2.imshow("video", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# ============================================================