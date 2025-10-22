import speech_recognition as sr
import pyttsx3
import openai
import numpy as np
import cv2
import pygame  #pip install pygame
from pygame import mixer
import RPi.GPIO as GPIO
import mediapipe as mp
import time
import random
from deep_translator import GoogleTranslator
from langdetect import detect
from adafruit_servokit import ServoKit

mixer.init()
mixer.music.load("/home/cex/Downloads/WeRtheRobots.mp3")
kit = ServoKit(channels=16)
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

cap=cv2.VideoCapture(0)
mp_drawing = mp.solutions.drawing_utils
mp_face = mp.solutions.face_detection.FaceDetection(model_selection=1,min_detection_confidence=0.5)
count=0
width=680
height=480

def obj_data(img):
    image_input = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = mp_face.process(image_input)
    if not results.detections:
       print("noface")
    else:    
         for detection in results.detections:
             bbox = detection.location_data.relative_bounding_box
#             print(bbox)
             x, y, w, h = int(bbox.xmin*width), int(bbox.ymin * height), int(bbox.width*width),int(bbox.height*height)
             cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
             cx=int(x+x+w)//2
             cy=int(y+y+h)//2
             #cv2.cSearch
       
             a=int(cx)//5
             b=int(cy)//5
             print("a",a)
             print("b",b)
             kit.servo[0].angle = a
             kit.servo[14].angle=180-a
             #kit.continuous_servo[0].throttle = 1
             kit.servo[1].angle=b
             kit.servo[13].angle=b
             #kit.continuous_servo[1].throttle = 1
             time.sleep(1)

#Initializing functiile pentru bibliotecile din text to speech
listening = True
engine = pyttsx3.init()

#Setam API-ul proiectului nostru cu OpenAI, si rolurile jucate de utilizatori si AI in acest proiect
openai.api_key = "xxxx"
messages = [{"role": "system", "content": "Your name is John and give answers in 3 lines"}]

#Customizam vocea AI-ului
voices = engine.getProperty('voices')
rate = engine.getProperty('rate')
volume = engine.getProperty('volume')

#for voice in voices:
#    engine.setProperty('voice',voice.id)
#    engine.say('buna dimineata Soare')
#engine.runAndWait()

def get_response(user_input):
    messages.append({"role": "user", "content": user_input})
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = messages
    )
    ChatGPT_reply = response["choices"][0]["message"]["content"]
    messages.append({"role": "assistant", "content": ChatGPT_reply})
    return ChatGPT_reply
def moveServoSlowly(unghi, startAngle, endAngle, stepDelay):
    if (startAngle < endAngle): 
        for i in range(startAngle, endAngle):
            #unghi=range(0,15)
            kit.servo[unghi].angle=i
            time.sleep(stepDelay)
    else:
        for i in range(startAngle, endAngle, -1):
            kit.servo[unghi].angle = i
            time.sleep(stepDelay)
    #servo 2 e dreaptaUmarX
    #servo 3 e dreapta cot
    #servo 4 e dreapta antebrat
    #5 sunt degetele drepte fata

def moveServoSlowly2(unghi1,unghi2,unghi3,unghi4,unghi5, startAngle, endAngle, stepDelay):
    if (startAngle < endAngle): 
        for i in range(startAngle, endAngle):
            #unghi=range(0,15)
            kit.servo[unghi1].angle=i
            kit.servo[unghi2].angle=i
            kit.servo[unghi3].angle=i
            kit.servo[unghi4].angle=i
            kit.servo[unghi5].angle=i
            time.sleep(stepDelay)
    else:
        for i in range(startAngle, endAngle, -1):
            kit.servo[unghi1].angle=i
            kit.servo[unghi2].angle=i
            kit.servo[unghi3].angle=i
            kit.servo[unghi4].angle=i
            kit.servo[unghi5].angle=i
            time.sleep(stepDelay)
def salutDreapta():

    moveServoSlowly(2, 0, 90, 0.02)
    moveServoSlowly(3, 0, 90, 0.02)
    moveServoSlowly(5, 150, 0, 0.02)
    time.sleep(0.5)
    print(1)
    for i in range(0, 3): 
        moveServoSlowly(3, 0, 45, 0.02)
        moveServoSlowly(3, 45, 0, 0.02)
        print(2)   
    moveServoSlowly(5, 0, 150, 0.02)
    time.sleep(1) 
    moveServoSlowly(3, 0, 150, 0.02)
    moveServoSlowly(2, 90, 0, 0.02)
    print(3)
#6 e umar stang
#7 e cot stang````
#8 e antebrat stang
#9 sunt degetele stangi fata
#uma r stang OY
def paharStanga():
    moveServoSlowly2(1,13,15,15,15,0,90,0.02)
    moveServoSlowly2(1,13,15,15,15,90,0,0.02)
    moveServoSlowly(6, 25, 0, 0.02)
    moveServoSlowly(7, 0, 90, 0.02)
    moveServoSlowly(10, 0, 90, 0.02)
    moveServoSlowly(8, 0, 45, 0.02)
    moveServoSlowly2(9,11,15,12,15,180,0,0.02)
    moveServoSlowly(10,90, 0, 0.02)
    moveServoSlowly(8, 45, 22, 0.02)
    #moveServoSlowly(6, 60, 150, 0.02)
    time.sleep(1)
    for i in range (0,10):
        moveServoSlowly(8,0,150,0.005)
    time.sleep(0.5)
    time.sleep(0.5)
  
  
    moveServoSlowly(6, 150, 0, 0.02)
    #moveServoSlowly(7, 90, 0, 0.02)
    moveServoSlowly(10, 0, 90, 0.02)
    moveServoSlowly(8, 22, 45, 0.02)
    moveServoSlowly2(9,11,12,15,15,0,180,0.02)
    #time.sleep(1)
    engine.say("here you go")
    engine.runAndWait()
    time.sleep(0.5)
    moveServoSlowly(10, 90, 0, 0.02)
    moveServoSlowly(7, 90, 0, 0.02)
    #moveServoSlowly(8, 45, 0, 0.02)


def dansezi():
    mixer.music.play()
    time.sleep(2)
    for i in range(0,5):
        engine.say("i'm a robot")
        moveServoSlowly(2, 0, 90, 0.005)
        moveServoSlowly2(1,13,15,15,15, 0, 90, 0.005)
        moveServoSlowly(3, 150, 0, 0.005)
        moveServoSlowly(3, 0, 150, 0.005)
        moveServoSlowly(10, 110, 180, 0.005)
        engine.say("and i'm dancing")
        moveServoSlowly2(1,13,15,15,15, 90, 180, 0.005)
        moveServoSlowly(7, 0, 90, 0.005)
        moveServoSlowly(7, 90, 0, 0.005)
        moveServoSlowly(2, 90, 0, 0.005)
        moveServoSlowly2(1,13,15,15,15, 150, 0, 0.005)
        moveServoSlowly(10, 180, 110, 0.005)
        engine.say("and i'm feeling good")
        engine.runAndWait()
    for i in range(0,10):
        moveServoSlowly(2, 0, 90, 0.005)
        moveServoSlowly2(1,13,15,15,15, 0, 90, 0.005)
        moveServoSlowly(3, 150, 0, 0.005)
        moveServoSlowly(3, 0, 150, 0.005)
        moveServoSlowly(10, 0, 90, 0.005)
        moveServoSlowly2(1,13,15,15,15, 90, 180, 0.005)
        moveServoSlowly(7, 0, 90, 0.005)
        moveServoSlowly(7, 90, 0, 0.005)
        moveServoSlowly(2, 90, 0, 0.005)
        moveServoSlowly2(1,13,15,15,15, 150, 0, 0.005)
        moveServoSlowly(10, 90, 0, 0.005)
    #for i  in range(0,5):
    #    moveServoSlowly(3, , 0, 0.02)

    

def joci():
    x=random.randint(0,2)
    moveServoSlowly2(9,11,15,15,15,180,0,0.02)
    moveServoSlowly2(15,15,12,15,15,0,180,0.02)
    moveServoSlowly(10, 110, 70, 0.02)
    moveServoSlowly(7, 90, 0, 0.02)
    moveServoSlowly(8, 0, 140, 0.02)
    moveServoSlowly(7, 0, 120, 0.02)
    engine.say("rock")
    engine.runAndWait()
    moveServoSlowly(7, 120, 0, 0.005)
    moveServoSlowly(7, 0, 120, 0.005)
    engine.say("paper")
    engine.runAndWait()
    moveServoSlowly(7, 120, 0, 0.005)
    moveServoSlowly(7, 0, 120, 0.005)
    engine.say("scissor")
    engine.runAndWait()
    moveServoSlowly(7, 120, 0, 0.005)
    engine.say("shoot")
    engine.runAndWait()
    moveServoSlowly(7, 0, 120, 0.005)
    if x == 2:
        moveServoSlowly(11, 0, 180, 0.005)
        print("foarfeca")
        engine.say("i chose scissor")
    elif x==1:
        moveServoSlowly2(9,11,12,15,15,0,180,0.01)
        print("hartie")
        engine.say("i chose paper")
    else: 
        print("piatra")
        engine.say("i chose rock")
    time.sleep(1)
    engine.runAndWait()
    moveServoSlowly(10, 70, 110, 0.02)
    moveServoSlowly2(9,11,15,15,12,0,180,0.01)
    moveServoSlowly(7, 120, 0, 0.01)
    moveServoSlowly(8, 140, 0, 0.02)


def multumesc():
    moveServoSlowly2(15,15,15,15,7, 0, 90, 0.02)
    moveServoSlowly2(15,15,15,15,6, 0, 20, 0.02)
    moveServoSlowly(10, 90, 45, 0.02)
    moveServoSlowly2(15,8,15,15,15, 0, 140, 0.02)
    moveServoSlowly2(15,11,9,12,15, 180, 0, 0.02)
    time.sleep(2)
    moveServoSlowly2(15,11,9,12,15, 0, 180, 0.01)
    moveServoSlowly2(15,15,15,15,7, 90, 0, 0.01)
    moveServoSlowly(10, 45, 90, 0.02)
    moveServoSlowly2(15,15,15,15,6, 20, 0, 0.01)
    moveServoSlowly2(15,8,15,15,15, 140, 0, 0.01)


while listening:

    ret,frame=cap.read()
    count += 1
    if count % 10 != 0:
        continue
    frame=cv2.resize(frame,(640,480))
    frame=cv2.flip(frame,-1)
    obj_data(frame)
     
    #cv2.imshow("FRAME",frame)
    if cv2.waitKey(1)&0xFF==27:
        engine.runAndWait()
        break

    with sr.Microphone() as source:
        recognizer = sr.Recognizer()
        recognizer.adjust_for_ambient_noise(source)
        recognizer.dynamic_energy_threshold = 3000
        kit.servo[0].angle = 40
        kit.servo[14].angle=140
        kit.servo[1].angle = 110
        kit.servo[13].angle = 70
        try:
            print("Listening...")
            audio = recognizer.listen(source, timeout=5.0)
            text = recognizer.recognize_google(audio, language='ro-RO')
            input_language = detect(text)
            print(text)
            textul_tradus=GoogleTranslator(source='ro',target='en').translate(text)
            kit.servo[0].angle = 110
            kit.servo[14].angle=70
            kit.servo[1].angle = 10
            kit.servo[13].angle=170

            print(textul_tradus)
            #kit.servo[5].angle=20
            #time.sleep(0.05)
            #kit.servo[5].angle=100

           
            if "john" in text.lower():
            
                response_from_openai = get_response(textul_tradus)
                engine.setProperty('rate',120)
                engine.setProperty('volume', volume)
                engine.setProperty('voice', 'american')
                engine.say(response_from_openai,'John')
                engine.runAndWait()
                kit.servo[0].angle = 150
                kit.servo[14].angle = 30
                kit.servo[1].angle = 170
                kit.servo[13].angle = 10
                if "salut" in text.lower():
                    print("salutMANA")
                    salutDreapta()
                if "shake" in text.lower():
                    print("aduPahar")
                    paharStanga()
                if "dansezi" in text.lower():
                    print("danez")
                    dansezi()
            if "mulțumesc" in text.lower():
                engine.say("you are welcome")
                print("multumesc")
                engine.runAndWait()
                multumesc()
            if "joci" in text.lower():
                    engine.say("sure, I'd like to play. I am always up for a challenge")
                    print("joaca")
                    engine.runAndWait()
                    joci()
                         
            else:
                print("Didn't recognize 'john'.")
           
        except sr.UnknownValueError:
            print("Didn't recognize anything.")
    
    
cap.release()
cv2.destroyAllWindows()






