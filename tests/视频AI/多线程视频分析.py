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
import math
from concurrent.futures import ThreadPoolExecutor, thread
# 保存好的视频检测人脸并截图

def getframesCount(video_path):
    video_cap=cv2.VideoCapture(video_path)
    # fps
    fps=video_cap.get(5)
    # frames total
    frames_total=video_cap.get(7)
    
def splitVideo(video_path,thread_num):
    '''
    split video into array
    '''
    video_cap=cv2.VideoCapture(video_path)
     # frames total
    frames_total=video_cap.get(7)
    print('total:%s' % frames_total)
    array=[]
    i=1
    frame_thread=math.ceil(frames_total/thread_num)
    while i<frames_total:

        array.append((i,frame_thread+i-1))
        if frames_total-i<frame_thread:
            array.append((i,frames_total-1))
        i+=frame_thread
    # for item in array:
    #     s,t=item
    #     print("%s %s" % (s,t))
    return array

def analyzeVideo(video_path,capt_folder,start_frame,end_frame):
    print('analy')
    video_cap=cv2.VideoCapture(video_path)
    video_cap.set(cv2.CAP_PROP_POS_FRAMES,start_frame)
    classfier=cv2.CascadeClassifier(r"G:\BaiduNetdiskDownload\weishitongAIVideo\haarcascade_frontalface_alt.xml")

    # 人脸边框，RGB
    color=(0,255,0)
    i=start_frame
    while video_cap.isOpened():
        success,frame=video_cap.read() # 读取一帧数据
        if  not success:
            return Exception("read failure")

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
                img_name="%s%d.jpg" % (video_path,i)
                # print(img_name)
                image=frame[y-10:y+h+10,x-10:x+w+10]
                # cv2.imwrite(img_name,image,[int(cv2.IMWRITE_PNG_COMPRESSION),9])

                # draw rectangle
                cv2.rectangle(frame,(x,y),(x+w,y+h),color,2)
                
                # display number of faces detected as a reminding
                font=cv2.FONT_HERSHEY_SIMPLEX
                # cv2.putText(frame,'num:%d/100' % (num),(x+30,y+30),font,1,(255,0,255),4)
               
                cv2.imwrite(capt_folder+"\\capt_%s.jpg" % i,frame,[int(cv2.IMWRITE_PNG_COMPRESSION),9])
        
        i+=1
        if i>end_frame:
            print("thread %s finished" % thread.__name__)
            break
    video_cap.release()
    


    



if __name__=="__main__":
    capt_foler=r"G:\BaiduNetdiskDownload\weishitongAIVideo\20210731191905"
    video_path=r"G:\BaiduNetdiskDownload\weishitongAIVideo\20210731191905.mp4"
    start_time=datetime.datetime.now()
    print(start_time)
    if os.path.exists(capt_foler):
        shutil.rmtree(capt_foler)
    
    os.makedirs(capt_foler)
    # catchPICFromVideo("get face",video_path,100,path)
    
    
    thread_count=10
    array=splitVideo(video_path,thread_count)
    thread_executor=ThreadPoolExecutor(max_workers=thread_count)
    for t in array:
        start,end=t
        thread_executor.submit(analyzeVideo,video_path,capt_foler,start,end)


    end_time=datetime.datetime.now()
    print(end_time)
    print("finished. %s elapsed" % (end_time-start_time).seconds)



    


