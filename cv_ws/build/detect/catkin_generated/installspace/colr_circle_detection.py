#!/usr/bin/env python3
import cv2
import numpy as np


def color_mask(color,img):
    r = color["R"]
    g = color["G"]
    b = color["B"]
    lower = np.array([b[0],g[0],r[0]])
    upper = np.array([b[1],g[1],r[1]])
    mask = cv2.inRange(img,lower,upper)
    imgResult = cv2.bitwise_and(img,img,mask=mask) # do the and operation for each pixel with the mask and the original image
    # cv2.imshow("mask",mask)
    # cv2.imshow("imgResult",imgResult)
    return imgResult, mask

def circle_estimation_mask(img, p1=100,p2=30,imgOut=None):
    

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # cv2.imshow("gray", gray)
    gray = cv2.medianBlur(gray, 5)
    # cv2.imshow("blur", gray)
    
    rows = gray.shape[0]
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, rows / 8,
                               param1=p1, param2=p2,
                               minRadius=0, maxRadius=0)
    
    # cv2.imshow(f"{p1}{p2}cgray", gray)
    if imgOut is not  None:
        img = imgOut

    if circles is not None:
        circles = np.uint16(np.around(circles))
        print(f"circles {p1} {p2}")
        for i in circles[0, :]:
            center = (i[0], i[1])
            # circle center
            cv2.circle(img, center, 1, (0, 100, 100), 3)
            # circle outline
            radius = i[2]
            cv2.circle(img, center, radius, (255, 0, 255), 3)
    return img

cap = cv2.VideoCapture(0) # wegcam 0
cap.set(3,640)#set video widht
cap.set(4,480)#set video height
# cap.set(10,100)#brightness 

# limites superiores e inferior da imagem
color = {"Azul" : {"R":(0,255),"G":(0,255),"B":(200,255)},
"Vermelho" : {"R":(200,255),"G":(0,255),"B":(0,255)},
"Verde" : {"R":(0,255),"G":(200,255),"B":(0,255)},
"Laranja" : {"R":(200,255),"G":(100,205),"B":(0,255)},
"All" : {"R":(0,255),"G":(0,255),"B":(0,255)}  }
x=60 #edge detector upper limit
y=28 #center detector th
while True:
    success, img = cap.read()
    # cv2.imshow("video", img)
    # img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    # imgHSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    imgresult, mask = color_mask(color["Verde"],img)
    # cv2.imshow("result", imgresult)
    # cv2.imshow("mask", mask)
    
    # caso queira estimativa de circulos feita sob a mascara, passar imgresult como entrada
    #caso n queira passar img;

    circleImg = circle_estimation_mask(imgresult,p1=x,p2=y, imgOut=imgresult)
    cv2.imshow(f"circles{x}{y}", circleImg)
    if cv2.waitKey(1) & 0xFF == ord('q'): #show img e break with q
        break
