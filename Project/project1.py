import cv2
import pygame
import mediapipe as mp
import sys

# 初期設定
pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Follow the Fish")

# 金魚の設定
fish_image = pygame.image.load('project/goldfish.png')  # 金魚の画像ファイル
fish_size = (100, 100)  # 金魚のサイズ（幅, 高さ）
fish_image = pygame.transform.scale(fish_image, fish_size)
fish_position = [width // 2, height // 2]

# MediaPipeの初期化
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

# ウェブカメラの初期化
cap = cv2.VideoCapture(0)

def detect_hand_position(frame):
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)
    
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # 人差し指の位置を取得（ここでは人差し指の先端）
            index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            # 座標の変換
            x = int(index_finger_tip.x * width)
            y = int(index_finger_tip.y * height)
            return (x, y)
    return None

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # ビデオフレームを左に90度回転
    frame_rotated = cv2.transpose(frame)         # 転置
    frame_rotated = cv2.flip(frame_rotated, 0)   # 上下反転

    # ビデオフレームをPygameに変換
    frame_rgb = cv2.cvtColor(frame_rotated, cv2.COLOR_BGR2RGB)
    frame_rgb = cv2.resize(frame_rgb, (width, height))  # リサイズ
    frame_surface = pygame.surfarray.make_surface(frame_rgb)

    # 手の位置を検出
    hand_position = detect_hand_position(frame_rotated)

    if hand_position:
        # 金魚の位置を指の位置に合わせる
        # ビデオフレームが左に90度回転したため、座標系を反転させる
        fish_position[0] = hand_position[1] - fish_size[0] // 2
        fish_position[1] = width - hand_position[0] - fish_size[1] // 2  # 上下反転の補正

        # 金魚のy軸の動きを反転させる
        fish_position[1] = height - fish_position[1] - fish_size[1]

    # ゲーム画面の更新
    screen.blit(frame_surface, (0, 0))  # ウェブカメラ映像を背景として描画
    screen.blit(fish_image, fish_position)  # 金魚を描画

    pygame.display.flip()

    # イベント処理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            cap.release()
            pygame.quit()
            sys.exit()

cap.release()
pygame.quit()
