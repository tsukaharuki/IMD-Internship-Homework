import cv2
import numpy as np
from PIL import Image
from keras.preprocessing.image import img_to_array
import imutils
from keras.models import load_model

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

emotion = '_mini_XCEPTION.102-0.66.hdf5'

#face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
face_detector = cv2.FaceDetectorYN_create("face_detection_yunet_2023mar.onnx", "", (320, 320), 0.6, 0.3, 5000, cv2.dnn.DNN_BACKEND_DEFAULT, target_id = cv2.dnn.DNN_TARGET_CPU)
emotion_classifier = load_model(emotion, compile=False)
EMOTIONS = ["angry", "disgust", "scared", "happy", "sad", "surprised", "neutral"]
pics = ('Resources/emo_oko.png', 'Resources/emo_ira.png', 'Resources/emo_kowai.png', 'Resources/emo_niko.png', 'Resources/emo_naki.png', 'Resources/emo_doki.png', 'Resources/emo_mu.png')
img = cv2.imread('Resources/A-pic.png')
#img = cv2.imread('Resources/odoroki.jpg')
maximum = 0

#gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#faces = face_cascade.detectMultiScale(gray, 1.1, 4)

face_detector.setInputSize((img.shape[1], img.shape[0]))
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
_, faces = face_detector.detect(img)
if len(faces) > 0:
    for rect in faces:
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
        emotion_probability = np.max(preds)
        label = EMOTIONS[preds.argmax()]

        for(i, (emotion, prob)) in enumerate(zip(EMOTIONS, preds)):
            text = "{}: {:.2f}%".format(emotion, prob * 100)
            print(text)
        
        cola = cv2.imread(pics[preds.argmax()], cv2.IMREAD_UNCHANGED)
        resized_cola = resize_image(cola, fW, fH)
        img = overlayOnPart(img, resized_cola, fX, fY)

cv2.imshow("Result", img)
cv2.waitKey(0)
