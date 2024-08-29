import cv2
import numpy as np
import pygame
import pymunk
import pymunk.pygame_util
import math

from Project.pymunk_test import space


def empty(a):   #トラックバーが変化したときにプログラムを更新する用
    pass

cap = cv2.VideoCapture(0)
cap.set(10,10) #明るさを設定。 ID10

cv2.namedWindow("TrackBars")        #トラックバーを表示するウィンドウを作る
cv2.resizeWindow("TrackBars",640,240)

cv2.createTrackbar("Hue Min","TrackBars",0,179,empty)   #トラックバーを作る(実装した結果最もオレンジをよくマスクできていた値をそれぞれの初期値としている)
cv2.createTrackbar("Hue Max","TrackBars",19,179,empty)
cv2.createTrackbar("Sat Min","TrackBars",110,255,empty)
cv2.createTrackbar("Sat Max","TrackBars",240,255,empty)
cv2.createTrackbar("Val Min","TrackBars",153,255,empty)
cv2.createTrackbar("Val Max","TrackBars",255,255,empty)
cv2.createTrackbar("perimeter Min","TrackBars",20,255,empty)     #検出する長方形の輪郭の周囲の長さの最小値


def detect_rects():
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # フレームをHSV色空間に変換

    h_min = cv2.getTrackbarPos("Hue Min", "TrackBars")  # トラックバーの位置の値を取得する
    h_max = cv2.getTrackbarPos("Hue Max", "TrackBars")
    s_min = cv2.getTrackbarPos("Sat Min", "TrackBars")
    s_max = cv2.getTrackbarPos("Sat Max", "TrackBars")
    v_min = cv2.getTrackbarPos("Val Min", "TrackBars")
    v_max = cv2.getTrackbarPos("Val Max", "TrackBars")
    min_perimeter = cv2.getTrackbarPos("perimeter Min", "TrackBars")

    lower_orange = np.array([h_min, s_min, v_min])  # トラックバーの値を配列に入れて色の範囲を決める
    upper_orange = np.array([h_max, s_max, v_max])

    # オレンジの部分だけをマスク
    mask = cv2.inRange(hsv, lower_orange, upper_orange)

    # マスクから輪郭を検出
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        arc_length = cv2.arcLength(contour, True)       #輪郭の周囲の長さを取得

        if arc_length > min_perimeter:      #周囲の長さが min_perimeter よりも大きい場合のみ処理を続行
            epsilon = 0.02 * arc_length     #近似のための許容範囲を設定
            approx = cv2.approxPolyDP(contour, epsilon, True)

            if len(approx) == 4 and cv2.isContourConvex(approx):        #長方形の条件: 4つの頂点を持ち、凸である
                cv2.drawContours(frame, [approx], -1, (0, 255, 0), 3)  #長方形を描画

                edgePos = []  # 長方形の各辺の始点と終点を行列に記録
                for i in range(4):
                    start_point = tuple(approx[i][0])  # 頂点の座標を取得
                    end_point = tuple(approx[(i + 1) % 4][0])  # 次の頂点の座標を取得
                    edgePos.append([start_point, end_point])

                edgePos = np.array(edgePos)         #行列に変換

                for i, (start, end) in enumerate(edgePos):       #各辺の始点と終点をループで出力
                    print(f"Edge {i + 1}: Start {start}, End {end}")
    return edgePos


# 線を追加する関数
def add_line(space, start, end):
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    shape = pymunk.Segment(body, start, end, 2)
    shape.elasticity = 0.95
    space.add(body, shape)  # ボディとシェイプを同時に追加
    return

def create_rects(matrix):
    for i, (start, end) in enumerate(matrix):
        add_line(space,start,end)



while True:
    ret, frame = cap.read()
    if not ret:
        break

    detect_rects()      #オレンジの長方形を検出

    if cv2.waitKey(1) == ord('t'):      #Tキーを押すとcreate_rectsを呼び出す
        create_rects(detect_rects())

    # 結果を表示
    cv2.imshow('Detected Rectangles', frame)

    # 'q'キーが押されたら終了
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# リソースを解放
cap.release()
cv2.destroyAllWindows()

