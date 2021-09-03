from sys import path
from PIL import Image
# py -m pip install pillow
import face_recognition
import os
import numpy as np
from numpy.core.defchararray import array
from numpy.lib.type_check import imag
import cv2

#
#安装face_recognition 需要先安装 py -m pip install cmake
#py -m pip install face_recognition
# Building wheel for dlib (setup.py) ... error
#最终解决方案：py -m pip install --no-dependencies face_recognition

# py -m pip install dlib
# py -m pip list
# pip install -i https://pypi.tuna.tsinghua.edu.cn/simple dlib


def face_detection(imagePath):
    image=face_recognition.load_image_file(imagePath)
    face_locations=face_recognition.face_locations(image)
    return len(face_locations)

def line_array(top,right,bottom,left):
    array=[]
    for i in range(5):
        row=top
        col=left
        while col<right:
            array.append((top+i,col+1))
            array.append((bottom+i,col+1))
            col=col+1

    for i in range(5):
        row=top
        col=left
        while row<bottom:
            array.append((row+1,col+i))
            array.append((row+1,right+i))
            row=row+1
    return array
color=(0,255,0)

if __name__=="__main__":
    path=r'G:\BaiduNetdiskDownload\weishitongAIVideo\IMG_20201125_180345.jpg'
    image=face_recognition.load_image_file(path)
    face_locations=face_recognition.face_locations(image)
    # face_locations=[(222,700,850,221)]
    # face_locations=[(222,700,1213,189)]
    print('i found {} face(s) in this photograph.'.format(len(face_locations)))
    for face_location in face_locations:
        top,right,bottom,left=face_location 
        #A list of tuples of found face locations in css (top,right,bottom,left) order
        # left top cornor point: (left,top);right bottom cornor point:(right,bottom)
        print('a face is located at pixel location top:{},left:{},Bottom:{},Right:{}'.format(top,left,bottom,right))

        face_image=image[top:bottom,left:right]
        pil_image=Image.fromarray(face_image)
        pil_image.show()
        # array=line_array(top,right,bottom,left)
        cv2.rectangle(image,(left,top),(right,bottom),color,2)
        # for t in array:
        #     r,c=t
        #     image[r,c]=(0,255,0)
        newImage=Image.fromarray(image)
        newImage.show()
        newImage.save(path)
       
    print('finished')
        

