import cv2
import cvzone
import numpy as np

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

totalMoney = 0

def empty(a):
    pass


cv2.namedWindow("Settings")
cv2.resizeWindow("Settings", 640, 240)
cv2.createTrackbar("Threshold1", "Settings", 219, 255, empty)
cv2.createTrackbar("Threshold2", "Settings", 233, 255, empty)

def preProcessing(img):

    imgPre = cv2.GaussianBlur(img, (5,5),3)
    thresh1 = cv2.getTrackbarPos("Threshold1", "Settings")
    thresh2 = cv2.getTrackbarPos("Threshold2", "Settings")
    imgPre = cv2.Canny(imgPre, 117, 255)
    kernel = np.ones((2,2),np.uint8)
    imgPre = cv2.dilate(imgPre,kernel,iterations=1)
    imgPre = cv2.morphologyEx(imgPre, cv2.MORPH_CLOSE, kernel)


    return imgPre
while True:
    sucess, img = cap.read()
    imgPre = preProcessing(img)
    imgContours, conFound = cvzone.findContours(img,imgPre,minArea=20)

    if conFound:
        for contour in conFound:
            peri = cv2.arcLength(contour['cnt'], True)
            approx = cv2.approxPolyDP(contour['cnt'], 0.02 * peri, True)

            if len(approx) > 5:
                area = contour['area']

                if 1500<area<1700:
                    totalMoney =10
                elif 1710<area<1900:
                    totalMoney =1
                elif 2000<area<2500:
                    totalMoney =5
                elif 2600<area<3200:
                    totalMoney =25
                else:
                    totalMoney =0
    print(totalMoney)


    imgStacked = cvzone.stackImages([img,imgPre,imgContours],2,1)
    cv2.imshow("image", imgStacked)

    cv2.waitKey(1)


