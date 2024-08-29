import cv2
import numpy as np
import pygame
import pymunk
import pymunk.pygame_util
import math

pygame.init()       #pygameを初期化

def empty(a):   #トラックバーが変化したときにプログラムを更新する用
    pass

run = True      #実行する

#Pymunkの空間を作成
space = pymunk.Space()
space.gravity = (0, 980)

#pygame用
WIDTH,HEIGHT = 800, 500
window = pygame.display.set_mode((WIDTH,HEIGHT))        #pygame用のウィンドウを作成
clock = pygame.time.Clock()

#OpenCV用
cap = cv2.VideoCapture(0)
cap.set(3,WIDTH)  #横幅を設定。ID3は横幅設定の項目
cap.set(4,HEIGHT)  #縦幅を設定。ID4は横幅設定の項目
cap.set(10,10) #明るさを設定。 ID10

#ボールスポーン座標
spawn_X=50
spawn_Y=10
ball_R=10   #ボール半径

#トラックバー関連
cv2.namedWindow("TrackBars")        #トラックバーを表示するウィンドウを作る
cv2.resizeWindow("TrackBars",640,240)

cv2.createTrackbar("Hue Min","TrackBars",0,179,empty)   #トラックバーを作る(実装した結果最もオレンジをよくマスクできていた値をそれぞれの初期値としている)
cv2.createTrackbar("Hue Max","TrackBars",80,179,empty)
cv2.createTrackbar("Sat Min","TrackBars",110,255,empty)
cv2.createTrackbar("Sat Max","TrackBars",240,255,empty)
cv2.createTrackbar("Val Min","TrackBars",90,255,empty)
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

                for i, (start, end) in enumerate(edgePos):      #ループでedgePosの値を代入してwindowに直線を描写する(ボディの予想線描いてくれる)
                    pygame.draw.line(window, (0, 255, 0), start, end, 1)

                return edgePos      #edgePosを返り値とする


def draw(space, window, draw_options):      #画面を白くする
    window.fill("white")
    space.debug_draw(draw_options)
    pygame.display.update()


#四角形の当たり判定を作るプログラム
def create_rects(matrix, space_cr):
    if matrix is None:  # matrixがNoneの場合(カメラが検出できてない)
        print("Can't find a rectangle!")
        return

    for i, (start, end) in enumerate(matrix):   #ループでmatrix(中身はedgePos)の値を代入
        add_line(space_cr, start, end)
        # print(f"Edge {i + 1}: Start {start}, End {end}")

# 線を追加する関数
def add_line(space_al, start, end):
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    shape = pymunk.Segment(body, start, end, 1)
    shape.elasticity = 0.8  #弾性
    shape.friction = 0.9  # 摩擦を追加
    shape.color = (0, 0, 0, 100)
    space.add(body, shape)  # ボディとシェイプを同時に追加
    return shape

# ボールを追加する関数
def create_ball(space, radius, mass):       #円を生成する関数
    body = pymunk.Body()        #body(物理情報を記録する所？質量、位置、向き、速度とかを持つ)を生成
    body.position = (spawn_X,spawn_Y)   #bodyの位置を設定
    shape = pymunk.Circle(body, radius) #shape(当たり判定)を作成
    shape.mass = mass
    shape.color = (255, 0, 0, 100)
    space.add(body, shape)      #body(物理情報)とshape(当たり判定)を持ったモデルを追加
    shape.elasticity = 0.9      #弾性を追加
    shape.friction = 0.9        #摩擦を追加
    return shape

# Pygame用の描画ヘルパー
draw_options = pymunk.pygame_util.DrawOptions(window)

#メイン
while run:      #runがtrueなら実行する
    ret, frame = cap.read()
    if not ret:
        break

    window.fill((255, 255, 255))    # 画面を白くする
    pygame.draw.circle(window, (255, 0, 0), (spawn_X, spawn_Y), ball_R)     #スポーン位置に円を描写


    # 常にイベントを受け付けるところ
    for event in pygame.event.get():
        if event.type == pygame.QUIT:       #キー入力でゲームを終了させる
            run = False
            break

        # ボタンをクリックしたとき
        if event.type == pygame.KEYDOWN:
            create_rects(detect_rects(), space)
            ball = create_ball(space, ball_R, 2)

    detect_rects()      #オレンジの長方形を検出

    # 結果を表示
    cv2.imshow('Detected Rectangles', frame)

    # 物理エンジンのステップ
    space.step(1/60.0)


    # 物理オブジェクトの描画
    space.debug_draw(draw_options)

    # 画面更新
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
