import cv2
from gtts import gTTS
from io import BytesIO
import pygame
from playsound import playsound
import os
import numpy as np
import pytesseract 

img = cv2.imread('./Capture.jpg');
language = 'en'
custom_config = r'--oem 3 --psm 6'
pytesseract.image_to_string(img,config = custom_config)

#Pre-Processing the Image .
#-- To get the grey scale image 
# DOCS -- https://docs.opencv.org/2.4/modules/imgproc/doc/miscellaneous_transformations.html
def get_grayscale(image):
    return cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)


def thresholding(image):
    return cv2.threshold(image,127,125,cv2.THRESH_BINARY)

def dilate(image):
    kernel = np.ones((5,5),np.unit8)
    return cv2.dilate(image,kernel,iterations = 1)

def opening(image):
    kernel = np.ones((5,5),np.unit8)
    return cv2.morphologyEx(image,cv2.MORPH_OPEN,kernel)

def canny(image):
    return cv2.Canny(image,100,200)

def deskew(image):
    coords = np.column_stack(np.where(image>0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    
    (h,w) = image.shape[:2]
    center = (w //2 , h//2)
    M = cv2.getRotationMatrix2D(center,angle , 1.0)
    rotated = cv2.wrapAffine(image,M,(w,h),flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated

#gray = get_grayscale(img)


h, w, c = img.shape

box = pytesseract.image_to_data(img,output_type="dict")
words = len(box['level'])
wix = box['text']
print(wix)

#pygame.init()
strings = 0
text = ''
for i in range (len(wix)):
    if wix[i] != '' :
        text = text + " " + wix[i]
        strings = strings + 1 
        #if strings < 4 :
        #    strings = 4if strings < 4:strings = 4 
    if strings > 3:
        print(strings)
        strings = 0
        myObj = gTTS(text=text , lang = language,slow=False)
        temp = BytesIO()
        myObj.write_to_fp(temp)
        temp.seek(0)
        pygame.mixer.init()
        pygame.mixer.music.load(temp)
        pygame.mixer.music.play()
        text = " "
        #myObj.save('spell.mp3')
        
        #os.remove('spell.mp3')

# Rest of the part is for the ViewPort of the Image
for i in range (words):
    (x,y,w,h) = (box['left'][i] , box['top'][i],box['width'][i] , box['height'][i])
    cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),1)

cv2.imshow('img', img)
cv2.waitKey(0)
cv2.destoryAllWindows()