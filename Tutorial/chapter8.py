import cv2
import numpy as np

def stackImages(scale,imgArray):    #画像を配列するファンクション(自作)
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver

def getContours(img):       #輪郭を検出する。引数は画像ファイル
    contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)      #輪郭を演出(RETR_EXTERNALは検出メゾットの種類)
    for cnt in contours:
        area = cv2.contourArea(cnt)     #検出した領域
        print(area)
        if area>500:    #検出された領域が500ピクセル以上なら
            cv2.drawContours(imgContour, cnt, -1, (0, 0, 255), 5)       #検出した輪郭を描写

            peri = cv2.arcLength(cnt,True)      #輪郭の弧の長さを取得
            #print(peri)
            approx = cv2.approxPolyDP(cnt,0.01*peri,True)       #形状を近似
            print(len(approx))
            objCor = len(approx)        #角の数を数える
            x, y, w, h = cv2.boundingRect(approx)

            if objCor ==3: objectType ="Tri"        #角が三つ検出されたばあい変数objectTypeをTriと名付ける
            elif objCor == 4:
                aspRatio = w/float(h)
                if aspRatio >0.98 and aspRatio <1.03: objectType= "Square"      #長方形の検出。aspRatioでアスペクト比を検出
                else:objectType="Rectangle"
            elif objCor>4: objectType= "Circles"
            else:objectType="None"

            cv2.rectangle(imgContour,(x,y),(x+w,y+h),(50,50,0),1)       #描画するboundingboxの設定
            cv2.putText(imgContour,objectType,      #objectType表示する
                        (x+(w//2)-10,y+(h//2)-10),cv2.FONT_HERSHEY_COMPLEX,0.7,(0,0,0),1)       #objectType表示位置の調整とフォント


path = 'Resources/shapes.png'
img = cv2.imread(path)
imgContour = img.copy()     #上から輪郭を表示するための元画像のコピー

imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)                  #グレイスケール化
imgBlur = cv2.GaussianBlur(imgGray,(7,7),1)         #ガウスフィルタ(ぼかし)
imgCanny = cv2.Canny(imgBlur,50,50)           #エッジ検出
getContours(imgCanny)

imgBlank = np.zeros_like(img)
imgStack = stackImages(0.6,([img,imgGray,imgBlur],  #画像を配列
                            [imgCanny,imgContour,imgBlank]))

cv2.imshow("Stack", imgStack)
cv2.waitKey(0)