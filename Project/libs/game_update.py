import numpy as np
import cv2

#クリック後の画像アップデート関数
def pic_update(pic_list,pos_list, height, width, splitx, splity, faces, img, elapsed_time):
    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)
    time_text = f"elapsed_time = {minutes:02}:{seconds:02}"

    org_cx, org_cy, width, height = faces[0]
    img_height, img_width, _ = img.shape
    info_space = 50 # ゲーム情報を描きだすための余白
    base_img = np.zeros((img_height+info_space, img_width, 3), np.uint8)
    base_img[info_space:info_space+img_height, 0:img_width] = img
    base_img[org_cy+info_space:org_cy+info_space+height, org_cx:org_cx+width] = 0
    cv2.putText(base_img, time_text, (img_width//3-10, 30),cv2.FONT_HERSHEY_SIMPLEX,fontScale=0.6,color=(255,255,0),thickness=2)

    cx, cy = org_cx, org_cy
    for j in range(splitx):
        for i in range(splity):
            ppp=splitx*j+i
            if pos_list[ppp]!=100:
                base_img[cy+info_space:cy+info_space+int(width/splitx),cx:cx+int(width/splitx),:]=pic_list[pos_list[ppp]]
            cy+=int(height/splity)
        cy=org_cy
        cx+=int(width/splitx)
    return base_img


#分割画像のポジション情報のアップデート
def pos_update(pos_index, pos_list, kkk, pos_available):
    if pos_available[pos_list.index(100)][pos_index]==1:
        pos_list[pos_list.index(100)]=pos_list[pos_index]
        pos_list[pos_index]=100
        kkk+=1
    return pos_list,kkk