# 
# 实际应用中，很多是通过视频流的方式进行识别，如门禁考勤，人脸动态跟踪识别

# 案例：opencv自带的haar人脸特征分类器，读取一段视频来识别其中的人脸

import datetime
from sys import path
import cv2
import os
from PIL import Image
import shutil
from datetime import date
# 保存好的视频检测人脸并截图

def catchPICFromVideo(window_name,camera_idx,catch_pic_num,skip_frame,path_name):
    # cv2.namedWindow(window_name)
    # video source
    video_cap=cv2.VideoCapture(camera_idx)
    
    # 人脸识别分类器
    classfier=cv2.CascadeClassifier(r"G:\BaiduNetdiskDownload\weishitongAIVideo\haarcascade_frontalface_alt.xml")

    # 人脸边框，RGB
    color=(0,255,0)
    i=0
    step=0
    if skip_frame:
        step=4
    while video_cap.isOpened():
        
        ok,frame=video_cap.read() # 读取一帧数据
        # 跳帧
        if skip_frame:
            video_cap.set(cv2.CAP_PROP_POS_FRAMES,i)
            success,frame=video_cap.read() # 读取一帧数据
        else:
            succes,frame=video_cap.read()
        if not ok:
            break
        # image=frame.crop((224,1022,732,316))
        grey=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY) # 将当前帧图像转换成灰度图像
        
        # face detection
        faceRects=classfier.detectMultiScale(grey,scaleFactor=1.2,minNeighbors=3,minSize=(32,32))
        if len(faceRects)>0: # 大于0则检测到人脸
            for faceRect in faceRects:
                x,y,w,h=faceRect

                if x<162 or y<162 or x+w>873 or y+h>641:
                    break 
                # 将当前帧保存为图片
                img_name="%s%d.jpg" % (path_name,i)
                # print(img_name)
                image=frame[y-10:y+h+10,x-10:x+w+10]
                # cv2.imwrite(img_name,image,[int(cv2.IMWRITE_PNG_COMPRESSION),9])

             
                # if num>(catch_pic_num):# 如果超过指定最大保存数量，退出循环
                #     break

                # draw rectangle
                cv2.rectangle(frame,(x,y),(x+w,y+h),color,2)
                
                # display number of faces detected as a reminding
                font=cv2.FONT_HERSHEY_SIMPLEX
                # cv2.putText(frame,'num:%d/100' % (num),(x+30,y+30),font,1,(255,0,255),4)
        
                cv2.imwrite(path_name+"\\capt_%s.jpg" % i,frame,[int(cv2.IMWRITE_PNG_COMPRESSION),9])

        # show image
        cv2.imshow(window_name,frame)
        
        c=cv2.waitKey(1)
        if c&0xFF==ord('q'):
            break
        i+=4
    video_cap.release()
    cv2.destroyAllWindows()


if __name__=="__main__":
    path=r"G:\BaiduNetdiskDownload\weishitongAIVideo\20210814195956"
    video_path=r"G:\BaiduNetdiskDownload\weishitongAIVideo\20210814195956.mp4"
    start=datetime.datetime.now()
    print(start)
    if os.path.exists(path):
        shutil.rmtree(path)
    else:
        os.makedirs(path)
    catchPICFromVideo("get face",video_path,100,True,path)
    end=datetime.datetime.now()
    print("finished. %s seconds elapsed" % (end-start).seconds)



