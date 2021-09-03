import os
import cv2
import time

def createVideo(path,size):
    filelist=os.listdir(path)
    '''
    fps
    帧率
    '''
    fps=20
    file_path=r"G:\BaiduNetdiskDownload\weishitongAIVideo\\"+str(int(time.time()))+".mp4"
    fourcc=cv2.VideoWriter_fourcc('D','I','V','X') # 不同视频编码对应不同视频格式
    video=cv2.VideoWriter(file_path,-1,fps,size)
    imgArray=[]
    for item in filelist:
        # if item.endswith('.jpg'):
    
        video.write(cv2.imread(path+"\\"+item))
    print('end')
    
if __name__=="__main__":
    createVideo(r"G:\BaiduNetdiskDownload\weishitongAIVideo\20210731180905",(1280,720))