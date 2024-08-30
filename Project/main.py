# ライブラリインポート
import cv2
import numpy as np
import random
import os
import time

from libs.game_update import pic_update, pos_update
from libs.get_video_img import get_video_img, split_pic

# ビデオをキャプチャして画像を作成・顔の座標を獲得
img_save_path = r"Resources\imgs\capture_img.jpg"
faces = get_video_img(img_save_path)

split_setting = 3

#画像の分割数指定、パズル用の情報入力
splitx=split_setting
splity=split_setting
counter=0
info_space = 50 # ゲーム情報を描きだすための余白

org_cx, org_cy, width, height = faces[0]

img = cv2.imread(img_save_path)
img_height, img_width, _ = img.shape

if split_setting == 3:
    #クリックした場所が何枚目なのか確認するための配列
    posx_list=[org_cx+width/6, org_cx+width/2, org_cx+width*5/6]
    posy_list=[org_cy+info_space+height/6, org_cy+info_space+height/2, org_cy+info_space+height*5/6]
    org_pos_list=[0,1,2,3,4,5,6,7,100]

    #移動可能な場所の指定(100が空いているマス、１は移動可能、０は移動負荷)
    pos_available = [[100,1,0,1,0,0,0,0,0],
                    [1,100,1,0,1,0,0,0,0],
                    [0,1,100,0,0,1,0,0,0],
                    [1,0,0,100,1,0,1,0,0],
                    [0,1,0,1,100,1,0,1,0],
                    [0,0,1,0,1,100,0,0,1],
                    [0,0,0,1,0,0,100,1,0],
                    [0,0,0,0,1,0,1,100,1],
                    [0,0,0,0,0,1,0,1,100]]
    
else:
    #クリックした場所が何枚目なのか確認するための配列
    posx_list=[org_cx+width/4, org_cx+width*3/4]
    posy_list=[org_cy+info_space+height/4, org_cy+info_space+height*3/4]
    org_pos_list=[0,1,2,100]

    #移動可能な場所の指定(100が空いているマス、１は移動可能、０は移動負荷)
    pos_available = [[100,1,1,0],
                     [1,100,0,1],
                     [1,0,100,1],
                     [0,1,1,100]]



#パズルゲームのメイン部分
def play_pazzle(event, x, y, flags, params):
    global counter, pos_list, kkk
    img2=np.copy(img)
    pic_list=split_pic(img, org_cx, org_cy, splitx, splity, height, width)

    #初期化
    if event == cv2.EVENT_LBUTTONDOWN and counter==0:
        pos_list=org_pos_list.copy()
        counter=1
        pos_index=0
        #ベース画像からランダムにマス目を移動させる
        kkk=0
        while kkk<100:
            pos_list,kkk=pos_update(pos_index, pos_list, kkk, pos_available)
            pos_index=np.random.randint(0,splitx*splity)  
        new_pic=pic_update(pic_list,pos_list, height, width, splitx, splity, faces, img)
        cv2.imshow('window', new_pic)
        print("init_OK")

    #マス目移動処理  
    elif event == cv2.EVENT_LBUTTONDOWN and counter==1:
        posx=np.argmin(np.abs(np.array(posx_list)-x))
        posy=np.argmin(np.abs(np.array(posy_list)-y))
        pos_index=posx*splitx+posy
        pos_list,kkk=pos_update(pos_index, pos_list, kkk, pos_available)
        new_pic=pic_update(pic_list,pos_list, height, width, splitx, splity, faces, img)
        cv2.imshow('window', new_pic)

        # 元の状態に戻ったら
        if pos_list==org_pos_list:
            cv2.putText(img2, 'Complete!!',(int(img_width/2)-150, int(img_height/2)+50),cv2.FONT_HERSHEY_SIMPLEX,fontScale=2,color=(0,255,0),thickness=6)
            cv2.imshow('window', img2)
            counter=0
            
#画像に番号をふっておく処理（なくてもOK）
for j in range(splitx):
    for i in range(splity):
        num=j*splitx+i
        cv2.putText(img, str(num) ,(int(org_cx + width/splitx*j + width/6), int(org_cy+height/splity*i + height/6)),cv2.FONT_HERSHEY_SIMPLEX,fontScale=1.0,color=(255,0,0),thickness=1)

cv2.imshow('window', img)
cv2.setMouseCallback('window', play_pazzle)
cv2.waitKey(0)
cv2.destroyAllWindows()