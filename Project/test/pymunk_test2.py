import pygame
import pymunk
import pymunk.pygame_util
import math

pygame.init()       #pygameを初期化

WIDTH,HEIGHT = 1000, 500
window = pygame.display.set_mode((WIDTH,HEIGHT))        #pygame用のウィンドウを作成

def create_ball(space, radius, mass):       #円を生成する関数
    body = pymunk.Body()        #body(物理情報を記録する所？質量、位置、向き、速度とかを持つ)を生成
    body.position = (300,300)   #bodyの位置を設定
    shape = pymunk.Circle(body, radius) #shape(当たり判定)を作成
    shape.mass = mass
    shape.color = (255, 0, 0, 100)
    space.add(body, shape)      #body(物理情報)とshape(当たり判定)を持ったモデルを追加
    shape.elasticity = 0.9      #弾性を追加
    shape.friction = 0.9        #摩擦を追加
    return shape

def create_boundaries(space, width, height):    #壁(boundaries)を生成する関数
    rects = [
        [(width/2, height - 5),(width, 10)],       #下の壁を作るための情報。[pos(長方形の中心位置),size(長方形の縦横長さ)]
        [(width/2, 5), (width, 10)],               #上の壁を作るための情報。
        [(5, height/2), (10, height)],             #左の壁を作るための情報。
        [(width - 5, height/2), (10, height)]      #右の壁を作るための情報。
    ]

    for pos, size in rects:    #ループでrects内の各壁の情報をpos,sizeに代入する
        body = pymunk.Body(body_type=pymunk.Body.STATIC)        #ボディを作成
        body.position = pos     #ボディの位置をposに設定
        shape = pymunk.Poly.create_box(body, size)      #大きさがsizeのshapeを作成
        shape.elasticity = 0.8      #弾性を追加
        shape.friction = 0.5        #摩擦を追加
        space.add(body,shape)       #body(物理情報)とshape(当たり判定)を持ったモデルを追加

def draw(space, window, draw_options):      #画面を白くする
    window.fill("white")
    space.debug_draw(draw_options)
    pygame.display.update()

def run(window, width, height):     #実行する関数
    run = True
    clock = pygame.time.Clock()
    fps = 60
    dt = 1/fps

    space = pymunk.Space()      #オブジェクトに重力や衝突を与える
    space.gravity = (0, 980)    #重力の設定

    ball = create_ball(space, 10, 2)
    create_boundaries(space, width, height)

    draw_options = pymunk.pygame_util.DrawOptions(window)       #描画機能の設定

    while run:      #どのパソコンでもfpsを60に固定
        for event in pygame.event.get():
            if event.type == pygame.QUIT:       #キー入力でゲームを終了させる
                run = False
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                print("MouseButtonDown")

        draw(space, window, draw_options)
        space.step(dt)
        clock.tick(fps)

    pygame.quit()

if __name__ == "__main__":
    run(window, WIDTH, HEIGHT)