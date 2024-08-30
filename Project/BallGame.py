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
WIDTH,HEIGHT = 680, 480
window = pygame.display.set_mode((WIDTH,HEIGHT))        #pygame用のウィンドウを作成
clock = pygame.time.Clock()

#ボールスポーン座標
spawn_X=50
spawn_Y=10
ball_R=10   #ボール半径

#トラックバー関連
cv2.namedWindow("TrackBars_red")        #トラックバーを表示するウィンドウを作る
cv2.resizeWindow("TrackBars_red",640,300)

cv2.namedWindow("TrackBars_blue")        #トラックバーを表示するウィンドウを作る
cv2.resizeWindow("TrackBars_blue",640,300)

#赤色を検出するためのトラックバーに使う変数
cv2.createTrackbar("Hue Min","TrackBars_red",30,179,empty)   #トラックバーを作る(実装した結果最も赤をよくマスクできていた値をそれぞれの初期値としている)
cv2.createTrackbar("Hue Max","TrackBars_red",80,179,empty)
cv2.createTrackbar("Sat Min","TrackBars_red",100,255,empty)
cv2.createTrackbar("Sat Max","TrackBars_red",255,255,empty)
cv2.createTrackbar("Val Min","TrackBars_red",100,255,empty)
cv2.createTrackbar("Val Max","TrackBars_red",255,255,empty)
cv2.createTrackbar("perimeter Min","TrackBars_red",80,255,empty)     #検出する長方形の輪郭の周囲の長さの最小値
cv2.createTrackbar("camera brightness","TrackBars_red",0,500,empty)

#青色を検出するためのトラックバーに使う変数
cv2.createTrackbar("Hue Min","TrackBars_blue",90,179,empty)   #トラックバーを作る(実装した結果最も赤をよくマスクできていた値をそれぞれの初期値としている)
cv2.createTrackbar("Hue Max","TrackBars_blue",150,179,empty)
cv2.createTrackbar("Sat Min","TrackBars_blue",200,255,empty)
cv2.createTrackbar("Sat Max","TrackBars_blue",255,255,empty)
cv2.createTrackbar("Val Min","TrackBars_blue",176,255,empty)
cv2.createTrackbar("Val Max","TrackBars_blue",255,255,empty)
cv2.createTrackbar("perimeter Min","TrackBars_blue",80,255,empty)     #検出する長方形の輪郭の周囲の長さの最小値

#OpenCV用
cap = cv2.VideoCapture(0)
cap.set(3,WIDTH)  #横幅を設定。ID3は横幅設定の項目
cap.set(4,HEIGHT)  #縦幅を設定。ID4は横幅設定の項目

def change_brightness():        #カメラの明るさを変更する関数
    camera_brightness = cv2.getTrackbarPos("camera brightness", "TrackBars_red")
    cap.set(10, camera_brightness)  # 明るさを設定。 ID10

def detect_red():       #赤い長方形を検出
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # フレームをHSV色空間に変換

    h_min_red = cv2.getTrackbarPos("Hue Min", "TrackBars_red")  # トラックバーの位置の値を取得する
    h_max_red = cv2.getTrackbarPos("Hue Max", "TrackBars_red")
    s_min_red = cv2.getTrackbarPos("Sat Min", "TrackBars_red")
    s_max_red = cv2.getTrackbarPos("Sat Max", "TrackBars_red")
    v_min_red = cv2.getTrackbarPos("Val Min", "TrackBars_red")
    v_max_red = cv2.getTrackbarPos("Val Max", "TrackBars_red")
    min_perimeter = cv2.getTrackbarPos("perimeter Min", "TrackBars_red")

    lower_red = np.array([h_min_red, s_min_red, v_min_red])  # トラックバーの値を配列に入れて色の範囲を決める
    upper_red = np.array([h_max_red, s_max_red, v_max_red])

    # 赤の部分だけをマスク
    mask_red = cv2.inRange(hsv, lower_red, upper_red)
    # マスクから輪郭を検出
    contours, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        arc_length = cv2.arcLength(contour, True)       #輪郭の周囲の長さを取得

        if arc_length > min_perimeter:      #周囲の長さが min_perimeter よりも大きい場合のみ処理を続行
            epsilon = 0.02 * arc_length     #近似のための許容範囲を設定
            approx = cv2.approxPolyDP(contour, epsilon, True)

            if len(approx) == 4 and cv2.isContourConvex(approx):        #長方形の条件: 4つの頂点を持ち、凸である
                cv2.drawContours(frame, [approx], -1, (0, 255, 0), 3)  #長方形を描画

                edgePos_red = []  # 長方形の各辺の始点と終点を行列に記録
                for i in range(4):
                    start_point = tuple(approx[i][0])  # 頂点の座標を取得
                    end_point = tuple(approx[(i + 1) % 4][0])  # 次の頂点の座標を取得
                    edgePos_red.append([start_point, end_point])

                for i, (start, end) in enumerate(edgePos_red):      #ループでedgePosの値を代入してwindowに直線を描写する(ボディの予想線描いてくれる)
                    pygame.draw.line(window, (0, 255, 0), start, end, 1)

                return edgePos_red      #edgePosを返り値とする

def detect_blue():      #青い長方形を検出
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # フレームをHSV色空間に変換

    h_min_blue = cv2.getTrackbarPos("Hue Min", "TrackBars_blue")  # トラックバーの位置の値を取得する
    h_max_blue = cv2.getTrackbarPos("Hue Max", "TrackBars_blue")
    s_min_blue = cv2.getTrackbarPos("Sat Min", "TrackBars_blue")
    s_max_blue = cv2.getTrackbarPos("Sat Max", "TrackBars_blue")
    v_min_blue = cv2.getTrackbarPos("Val Min", "TrackBars_blue")
    v_max_blue = cv2.getTrackbarPos("Val Max", "TrackBars_blue")
    min_perimeter = cv2.getTrackbarPos("perimeter Min", "TrackBars_blue")

    lower_blue = np.array([h_min_blue, s_min_blue, v_min_blue])  # トラックバーの値を配列に入れて色の範囲を決める
    upper_blue = np.array([h_max_blue, s_max_blue, v_max_blue])

    # 青の部分だけをマスク
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
    # マスクから輪郭を検出
    contours, _ = cv2.findContours(mask_blue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        arc_length = cv2.arcLength(contour, True)       #輪郭の周囲の長さを取得

        if arc_length > min_perimeter:      #周囲の長さが min_perimeter よりも大きい場合のみ処理を続行
            epsilon = 0.02 * arc_length     #近似のための許容範囲を設定
            approx = cv2.approxPolyDP(contour, epsilon, True)

            if len(approx) == 4 and cv2.isContourConvex(approx):        #長方形の条件: 4つの頂点を持ち、凸である
                cv2.drawContours(frame, [approx], -1, (0, 255, 0), 3)  #長方形を描画

                edgePos_blue = []  # 長方形の各辺の始点と終点を行列に記録
                for i in range(4):
                    start_point = tuple(approx[i][0])  # 頂点の座標を取得
                    end_point = tuple(approx[(i + 1) % 4][0])  # 次の頂点の座標を取得
                    edgePos_blue.append([start_point, end_point])

                for i, (start, end) in enumerate(edgePos_blue):      #ループでedgePosの値を代入してwindowに直線を描写する(ボディの予想線描いてくれる)
                    pygame.draw.line(window, (0, 255, 0), start, end, 1)

                return edgePos_blue      #edgePosを返り値とする

#画面を白くする
def draw(space, window, draw_options):
    window.fill("white")
    space.debug_draw(draw_options)
    pygame.display.update()

#四角形の当たり判定を作るプログラム
def create_rects(matrix, space_cr, elast_cr, color_cr):
    if matrix is None:  # matrixがNoneの場合(カメラが検出できてない)
        print("Can't find a rectangle!")
        return

    for i, (start, end) in enumerate(matrix):   #ループでmatrix(中身はedgePos)の値を代入
        add_line(space_cr, start, end, elast_cr, color_cr)

# 線を追加する関数
def add_line(space_al, start, end, elast_al, color_al):
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    shape = pymunk.Segment(body, start, end, 3)
    shape.elasticity = elast_al  #弾性
    shape.friction = 0.9  # 摩擦を追加
    shape.color = (color_al)
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

#ステージを作る関数
def create_stage():
    wall= [
        [(200, 300),(10,350)],       #壁を作るための情報。[pos(長方形の中心位置),size(長方形の縦横長さ)]
        [(200, 20), (10, 30)],
    ]
    for pos, size in wall:    #ループでrects内の各壁の情報をpos,sizeに代入する
        body = pymunk.Body(body_type=pymunk.Body.STATIC)        #ボディを作成
        body.position = pos     #ボディの位置をposに設定
        shape = pymunk.Poly.create_box(body, size)      #大きさがsizeのshapeを作成
        shape.elasticity = 0.7      #弾性を追加
        shape.friction = 0.5        #摩擦を追加
        space.add(body,shape)       #body(物理情報)とshape(当たり判定)を持ったモデルを追加

    goals = [
        [(650, 80), (10, 90)],       #ゴールを作るための情報。[pos(長方形の中心位置),size(長方形の縦横長さ)]
        [(600, 100), (10, 40)],
        [(620, 120), (50, 10)],
        [(620, 40), (50, 10)],
    ]
    for pos, size in goals:    #ループでrects内の各壁の情報をpos,sizeに代入する
        body = pymunk.Body(body_type=pymunk.Body.STATIC)        #ボディを作成
        body.position = pos     #ボディの位置をposに設定
        shape = pymunk.Poly.create_box(body, size)      #大きさがsizeのshapeを作成
        shape.elasticity = 0.2      #弾性を追加
        shape.friction = 0.5        #摩擦を追加
        shape.color = (0, 255, 255, 100)
        space.add(body,shape)       #body(物理情報)とshape(当たり判定)を持ったモデルを追加


# Pygame用の描画ヘルパー
draw_options = pymunk.pygame_util.DrawOptions(window)
create_stage()

#メイン
while run:      #runがtrueなら実行する
    ret, frame = cap.read()
    if not ret:
        break

    window.fill((255, 255, 255))  # 画面を白くする
    pygame.draw.circle(window, (255, 0, 0), (spawn_X, spawn_Y), ball_R)  # スポーン位置に円を描写

    # 常にイベントを受け付けるところ
    for event in pygame.event.get():
        if event.type == pygame.QUIT:       #キー入力でゲームを終了させる
            run = False
            break

        # ボタンをクリックしたとき
        if event.type == pygame.KEYDOWN:
            if detect_red() != None:
                create_rects(detect_red(),space,1.2, (0,255,0,100))

            elif detect_blue() != None:
                create_rects(detect_blue(),space,0.5, (0,0,255,100))

            ball = create_ball(space, ball_R, 2)


    change_brightness()     #カメラの明かるさを変更
    detect_red()      #赤の長方形を検出
    detect_blue()


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
