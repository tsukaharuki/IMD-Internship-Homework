import pygame
import pymunk
import pymunk.pygame_util
from pymunk.vec2d import Vec2d

# Pygameの初期化
pygame.init()

# ウィンドウの設定
window_width, window_height = 1000, 400
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("BallGame")
clock = pygame.time.Clock()

# Pymunkの空間を作成
space = pymunk.Space()
space.gravity = (0, 900)

# ボールを追加する関数
def add_ball(space, position):
    mass = 1
    radius = 15
    inertia = pymunk.moment_for_circle(mass, 0, radius)
    body = pymunk.Body(mass, inertia)
    body.position = position
    shape = pymunk.Circle(body, radius)
    shape.elasticity = 0.95
    space.add(body, shape)  # ボディとシェイプを同時に追加
    return shape

# 線を追加する関数
def add_line(space, start, end):
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    shape = pymunk.Segment(body, start, end, 1)
    shape.elasticity = 0.95
    space.add(body, shape)  # ボディとシェイプを同時に追加
    return shape

# ボールと線の作成
ball = add_ball(space, (300, 100))
line = add_line(space, (100, 300), (500, 350))

# Pygame用の描画ヘルパー
draw_options = pymunk.pygame_util.DrawOptions(screen)

# ゲームループ
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
            running = False

    # 物理エンジンのステップ
    space.step(1/50.0)

    # 画面のクリア
    screen.fill((255, 255, 255))

    # 物理オブジェクトの描画
    space.debug_draw(draw_options)

    # 画面更新
    pygame.display.flip()
    clock.tick(50)

pygame.quit()
