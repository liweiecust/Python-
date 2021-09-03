import cv2
import os,sys
import shutil
from 测试人脸检测 import face_detection
from concurrent.futures import ThreadPoolExecutor


print('sdf')
imagePath=r"G:\BaiduNetdiskDownload\weishitongAIVideo\20210731174905"

executor=ThreadPoolExecutor(max_workers=20)

def removefile(path):
    os.remove(path)


for root,dirs,file_list in os.walk(imagePath):
    for file_name in file_list:
        path=os.path.join(root,file_name)
        face_count=face_detection(path)
        if face_count==0:
            # os.remove(path)
            executor.submit(os.remove,(path))
        else:
            print("%s faces found in %s" % (face_count,file_name))
print('finished')