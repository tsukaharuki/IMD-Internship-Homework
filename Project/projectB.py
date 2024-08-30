from keras.preprocessing.image import img_to_array
import imutils
from keras.models import load_model
from PIL import Image
import cv2
import numpy as np

def resize_image(image, height, width):
    org_height, org_width = image.shape[:2]

    if float(height)/org_height > float(width)/org_width:
        ratio = float(height)/org_height
    else:
        ratio = float(width)/org_width
    
    resized = cv2.resize(image, (int(org_height*ratio), int(org_width*ratio)))
    return resized

def overlayOnPart(src_image, overlay_image, posX, posY):
    ol_h, ol_w = overlay_image.shape[:2]
    src_image_RGBA = cv2.cvtColor(src_image, cv2.COLOR_BGRA2RGBA)
    overlay_image_RGBA = cv2.cvtColor(overlay_image, cv2.COLOR_BGRA2RGBA)

    src_image_PIL = Image.fromarray(src_image_RGBA)
    overlay_image_PIL = Image.fromarray(overlay_image_RGBA)

    src_image_PIL = src_image_PIL.convert('RGBA')
    overlay_image_PIL = overlay_image_PIL.convert('RGBA')

    tmp = Image.new('RGBA', src_image_PIL.size, (255, 255, 255, 0))
    tmp.paste(overlay_image_PIL, (posX, posY), overlay_image_PIL)
    result = Image.alpha_composite(src_image_PIL, tmp)

    return cv2.cvtColor(np.asarray(result), cv2.COLOR_RGBA2BGRA)

face_detector = cv2.FaceDetectorYN_create("face_detection_yunet_2023mar.onnx", "", (320, 320), 0.6, 0.3, 5000, cv2.dnn.DNN_BACKEND_DEFAULT, target_id = cv2.dnn.DNN_TARGET_CPU)
emotion = '_mini_XCEPTION.102-0.66.hdf5'

emotion_classifier = load_model(emotion, compile=False)
EMOTIONS = ["angry", "disgust", "scared", "happy", "sad", "surprised", "neutral"]
pics = ('Resources/emo_oko.png', 'Resources/emo_ira.png', 'Resources/emo_kowai.png', 'Resources/emo_niko.png', 'Resources/emo_naki.png', 'Resources/emo_doki.png', 'Resources/emo_mu.png')

cv2.namedWindow('Camera')
cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
while True:
    frame = cam.read()[1]
    face_detector.setInputSize((int(cam.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, faces = face_detector.detect(frame)
    frameClone = frame.copy()
    if type(faces) is not np.ndarray:
        p = 1
    elif len(faces) > 0:
        for rect in faces:
            suitable = 0
            p = 1
            fX = int(rect[0])
            fY = int(rect[1])
            fW = int(rect[2])
            fH = int(rect[3])
        
            roi = gray[fY:fY + fH, fX:fX + fW]
            roi = cv2.resize(roi, (64, 64))
            roi = roi.astype("float") / 255.0
            roi = img_to_array(roi)
            roi = np.expand_dims(roi, axis = 0)

            preds = emotion_classifier.predict(roi)[0]

            i = 0
            while True:
                if i >= len(pics)-1:
                    break
                elif preds[i] > 0.22 and preds[i] >= preds[suitable]:
                    if (suitable == 3 and preds[i]*1.5 >= preds[suitable]) or (i == 3 and preds[i] >= preds[suitable]*1.5):
                        suitable = i
                        p = 0
                    elif suitable != 3 and i != 3 and preds[i] >= preds[suitable]:
                        suitable = i
                        p = 0

                i = i + 1
            if p == 1:
                suitable = len(pics)-1
            cola = cv2.imread(pics[suitable], cv2.IMREAD_UNCHANGED)
            resized_cola = resize_image(cola, fW, fH)
            frameClone = overlayOnPart(frameClone, resized_cola, fX, fY)

    
    cv2.imshow('camera', frameClone)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()

