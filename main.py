import cv2
import pyttsx3
import numpy as np
import pytesseract 

img = cv2.imread('./Capture.jpg');
language = 'en'
custom_config = r'--oem 3 --psm 6'
pytesseract.image_to_string(img,config = custom_config)

#Speaking Engine .
engine = pyttsx3.init()
print(engine.getProperty('rate'))
engine.setProperty('rate' , 150)
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[0].id)

def speakSomething(text):
    engine.say(text)
    engine.runAndWait()

#Image Maipulation Channel .
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


h, w, c = img.shape
word = '' 
stringData = pytesseract.image_to_data(img,output_type="dict")
words = len(stringData['level'])
# Rest of the part is for the ViewPort of the Image
for i in range (words):
    (x,y,w,h) = (stringData['left'][i] , stringData['top'][i],stringData['width'][i] , stringData['height'][i])
    cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),1)
cv2.imshow('img', img)

#To text
lengthOfData = len(stringData['text'])
firstPhase = True
sentence = ''
for i in range(lengthOfData):
    if stringData['word_num'][i] != 0 :
        sentence = sentence + " " + stringData['text'][i]
        if firstPhase:
            firstPhase = False 
    elif stringData['word_num'][i] == 0 and not firstPhase:
        speakSomething(sentence)
        sentence = ""
        print("beep")
engine.stop()