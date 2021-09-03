import cv2 # py -m pip install opencv-python
# 可能默认下载的模块跟你的Python环境不匹配，到下面的镜像中找和你版本匹配
import os,sys
import shutil
import datetime

# img=cv2.imread(r'G:\BaiduNetdiskDownload\beauty\mmexport1628082858289.png',cv2.IMREAD_UNCHANGED)
# cv2.imshow('image',img) # 路径中不要有中文
#input video
videoName=r"G:\BaiduNetdiskDownload\weishitongAIVideo\1628348593.mp4"
savedpath=r"G:\BaiduNetdiskDownload\weishitongAIVideo\1628348593"

# 计时
start_time=datetime.datetime.now()
isExists=os.path.exists(savedpath)
if not isExists:
    os.makedirs(savedpath)
    print('path of %s is build' % savedpath)
else:
    shutil.rmtree(savedpath)
    os.makedirs(savedpath)
    print('path of %s already exists and rebuild' % savedpath)

fps=14.91

# the gap of frame
count=10
video_cap=cv2.VideoCapture(videoName)
skip_frame=True
step=4
# print(videoCapture.size())
i=0
j=0

while True:
    success,frame=video_cap.read()
    # 跳帧
    if skip_frame:
        video_cap.set(cv2.CAP_PROP_POS_FRAMES,i)
        success,frame=video_cap.read() # 读取一帧数据
    else:
        succes,frame=video_cap.read()
   
    if not success:
        print('video is all read')
        break
    if(i%count==0):
        j+=1
    savedname=savedpath.split('\\')[3]+'_'+str(j)+'_'+str(i)+'.jpg'
    imgPath=savedpath+"\\"+savedname
    cv2.imwrite(imgPath,frame)
    # cv2.imshow('image',imgPath)
    print('image of %s is being saved' % imgPath)
    i+=step

end_time=datetime.datetime.now()
print(end_time)
print("finished. %s seconds elapsed" % (end_time-start_time).seconds)




