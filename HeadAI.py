import speech_recognition as sr
import pyttsx3
import openai
import cv2
import RPi.GPIO as GPIO
import mediapipe as mp
import time
from deep_translator import GoogleTranslator
from langdetect import detect
from adafruit_servokit import ServoKit


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
             cv2.circle(img,(cx,cy),5,(0,0,255),-1)
             a=int(cx)//5
             b=int(cy)//5
             print("a",a)
             print("b",b)
             kit.servo[0].angle = a
             #kit.continuous_servo[0].throttle = 1
             kit.servo[1].angle = b
             #kit.continuous_servo[1].throttle = 1
             time.sleep(1)

#Initializing functiile pentru bibliotecile din text to speech
listening = True
engine = pyttsx3.init()

#Setam API-ul proiectului nostru cu OpenAI, si rolurile jucate de utilizatori si AI in acest proiect
openai.api_key = "xxxxx"
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
        break

    with sr.Microphone() as source:
        recognizer = sr.Recognizer()
        recognizer.adjust_for_ambient_noise(source)
        recognizer.dynamic_energy_threshold = 3000
        kit.servo[0].angle = 90
        kit.servo[1].angle = 10
        try:
            print("Listening...")
            audio = recognizer.listen(source, timeout=5.0)
            text = recognizer.recognize_google(audio, language='ro-RO')
            input_language = detect(text)
            print(text)
            textul_tradus=GoogleTranslator(source='ro',target='en').translate(text)
            kit.servo[0].angle = 40
            kit.servo[1].angle = 90
            print(textul_tradus)
           
            if "john" in text.lower():
            
                response_from_openai = get_response(textul_tradus)
                engine.setProperty('rate', 120)
                engine.setProperty('volume', volume)
                engine.setProperty('voice', 'american')
                engine.say(response_from_openai,'John')
                engine.runAndWait()
                kit.servo[0].angle = 150
                kit.servo[1].angle = 170
                         
            else:
                print("Didn't recognize 'john'.")
           
        except sr.UnknownValueError:
            print("Didn't recognize anything.")
    
    
cap.release()
cv2.destroyAllWindows()
