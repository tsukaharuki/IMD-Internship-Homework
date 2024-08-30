import cv2
import pygame
import random
import mediapipe as mp
from pygame.locals import *
import time

# 定数
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BG_COLOR = (135, 206, 250)
GAME_OVER_COLOR = (255, 0, 0)
CLEAR_COLOR = (0, 255, 0)
TIMER_COLOR = (0, 0, 0)  # 残り時間の色
FONT_SIZE = 60

# Setup for sounds. Defaults are good.
pygame.mixer.init()
pygame.mixer.music.load("Project/maou.mp3")
pygame.mixer.music.play(loops=-1)
collision_sound = pygame.mixer.Sound("Project/damage.mp3")

# Pygameの初期化
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Mediapipeの初期化
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# カメラの初期化
cap = cv2.VideoCapture(0)

# プレイヤークラス
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        original_image = pygame.image.load("Project/dog.png").convert()
        self.surf = pygame.transform.scale(original_image, (60, 60))
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
    
    def update(self, move_x, move_y):
        self.rect.move_ip(move_x, move_y)
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

# 敵キャラクタークラス
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        original_image = pygame.image.load("Project/zombiedog.png").convert()
        self.surf = pygame.transform.scale(original_image, (50, 50))
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT)
            )
        )
        self.speed = random.randint(5, 20)
    
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

# プレイヤーのインスタンス
player = Player()

# グループの作成
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# 敵を定期的に生成するイベント
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 1000)  # 1秒ごとに敵を生成

# 初期の移動量
move_x, move_y = 0, 0

# ゲームオーバー・ゲームクリアのフラグ
game_over = False
game_clear = False

# ゲーム開始時刻の取得
start_time = time.time()

running = True
while running:
    if not game_over and not game_clear:
        ret, frame = cap.read()
        if not ret:
            break

        # フレームを反転
        frame = cv2.flip(frame, 1)

        # Mediapipeで手を検出
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)

        # 初期値に基づいた移動
        move_x, move_y = 0, 0

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                
                # 人差し指のランドマークを取得
                index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                
                # 画面サイズに合わせて座標をスケーリング
                index_x = int(index_finger_tip.x * SCREEN_WIDTH)
                index_y = int(index_finger_tip.y * SCREEN_HEIGHT)
                
                # 画面の中心と指の位置の差分を移動量に変換
                center_x = SCREEN_WIDTH // 2
                center_y = SCREEN_HEIGHT // 2
                move_x = (index_x - center_x) // 20
                move_y = (index_y - center_y) // 20

                # 手の位置に円を描画
                cv2.circle(frame, (index_x, index_y), 7, (0, 255, 0), -1)

        # Pygameのイベント処理
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == ADDENEMY:
                new_enemy = Enemy()
                enemies.add(new_enemy)
                all_sprites.add(new_enemy)

        # プレイヤーの位置を更新
        player.update(move_x, move_y)
        
        # 敵の位置を更新
        enemies.update()

        # 残り時間の計算
        elapsed_time = time.time() - start_time
        remaining_time = max(0, 30 - int(elapsed_time))

        # 画面を描画
        screen.fill(BG_COLOR)
        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)
        
        # 残り時間を描画
        font = pygame.font.SysFont(None, FONT_SIZE // 2)
        timer_text = font.render(f"Time Left: {remaining_time}s", True, TIMER_COLOR)
        screen.blit(timer_text, (10, 10))

        # 衝突判定
        if pygame.sprite.spritecollideany(player, enemies):
            player.kill()
            collision_sound.play()
            game_over = True
            # フレームを保存
            if frame is not None:
                cv2.imwrite("Project/game_over_screenshot.png", frame)

        # ゲームクリア判定
        if elapsed_time >= 30:
            game_clear = True
            # フレームを保存
            if frame is not None:
                cv2.imwrite("Project/game_clear_screenshot.png", frame)

        # ディスプレイの更新
        pygame.display.flip()
        
        # OpenCVのウィンドウにフレームを表示
        cv2.imshow("Finger Tracking", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        clock.tick(30)
    else:
        # ゲームオーバーまたはクリア画面の表示
        screen.fill(BG_COLOR)
        font = pygame.font.SysFont(None, FONT_SIZE)
        if game_clear:
            text = font.render("Game Clear", True, CLEAR_COLOR)
        else:
            text = font.render("Game Over", True, GAME_OVER_COLOR)
        text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        screen.blit(text, text_rect)
        pygame.display.flip()
        
        # 画面が表示されるのを待つ
        pygame.time.wait(2000)  # 2秒待つ

        # ゲームを終了する
        running = False

cap.release()
cv2.destroyAllWindows()
pygame.quit()
