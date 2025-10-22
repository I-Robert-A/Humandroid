import cv2
import mediapipe as mp
import time
import pyrebase
firebaseConfig={
   "apiKey": "****",
  "authDomain": "***",
  "databaseURL": "***",
  "projectId": "mana-7f65b",
  "storageBucket": "mana-7f65b.appspot.com",
  "messagingSenderId": "80786440933",
  "appId": "1:80786440933:web:8e6333bf402d27c13eca0c",
  "measurementId": "G-D3SB111182"
}
firebase=pyrebase.initialize_app(firebaseConfig)
db=firebase.database()
cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils
i=0
x=0
d=0
x2=0
d1=0
d2=0
d3=0
d4=0
dd=0
y=0
y2=0
a=0
a2=0
r=0
r2=0
p=0
p2=0
q=0
q2=0
pTime = 0
cTime = 0
while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    # print(results.multi_hand_landmarks)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                i=i+1
                # print(id, lm)
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                if id==8:
                   y=cy
                if id==5:
                   y2=cy
                if id==12:
                   a=cy
                if id==9:
                   a2=cy
                if id==16:
                   r=cy
                if id==13:
                   r2=cy
                if id==20:
                   p=cy
                if id==17:
                   p2=cy
                if id==4:
                   x=cx
                   q=cy
                if id==2:
                   x2=cx
                   q2=cy
                d=y2-y
                d1=a2-a
                d2=r2-r
                d3=p2-p
                d4=q2-q
                dd=x2-x
                data={"degetAR":d,"degetMij":d1,"degetI":d2,"degetMic":d3,"degetMareX":dd,"degetMAreY":d4}
                if i==200:
                   db.update(data)
                   i=0
                #db.update(data)
                #if d<=8:
                 #  print('degetulA e jos')
                #if d1<=8:
                 #  print('degetulMij e jos')
                #if d2<=8:
                 #  print('degetulI e jos')
                #if d3<=8:
                 #  print('degetulmic e jos')
                #if d4<=8 and dd>0 :
                  # print('degetulMARE e jos')
                print(dd, d4)
                # if id == 4:
                cv2.circle(img, (cx, cy), 15, (0, 0, 255), cv2.FILLED)

            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

    cTime = time.time()
    fps = 1/ (cTime - pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                (255, 0, 255), 3)
    img = cv2.flip(img,1)
    cv2.imshow("Image", img)
    cv2.waitKey(1)
