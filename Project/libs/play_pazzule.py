import cv2
import numpy as np

#パズルゲームのメイン部分
def play_pazzle(event, x, y, flags, params):
    global counter, pos_list, kkk
    img2=np.copy(img)
    pic_list=split_pic(img)

    #初期化
    if event == cv2.EVENT_LBUTTONDOWN and counter==0:
        pos_list=[0,1,2,3,4,5,6,7,100]
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
        print(f"現在のパズル状態：{pos_list}")
        cv2.imshow('window', new_pic)
        if pos_list==[0,1,2,3,4,5,6,7,100]:
            cv2.putText(img2, 'Complete!!',(int(img_width/2)-150, int(img_height/2)+50),cv2.FONT_HERSHEY_SIMPLEX,fontScale=2,color=(0,255,0),thickness=6)
            cv2.imshow('window', img2)
            counter=0