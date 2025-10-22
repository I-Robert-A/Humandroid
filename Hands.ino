COD PENTRU SALUT,MUTARE OBIECT
#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

// Definirea canalelor pentru servomotoare
const int channelServoStangaUmarX = 0;
const int channelServoStangaUmarY = 1;
const int channelServoDreaptaUmarX = 2;
const int channelServoDreaptaUmarY = 3;
const int channelServoStangaCot = 4;
const int channelServoDreaptaCot = 5;
const int channelServoStangaAntebrat = 6;
const int channelServoDreaptaAntebrat = 7;
const int channelServoStangaDeget1 = 8;
const int channelServoStangaDeget2 = 9;
const int channelServoStangaDeget3 = 10;
const int channelServoStangaDeget4 = 11;
const int channelServoStangaDeget5 = 12;

// Pinul de intrare pentru modulul de detecție a sunetului
const int soundSensorPin = 2;

// Crearea obiectului pentru PCA9685
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

void setup() {
  // Inițializare comunicare I2C
  Wire.begin();
  
  // Inițializare PCA9685
  pwm.begin();
  pwm.setPWMFreq(60); // Setare frecvență la 60 Hz pentru servomotoare

  // Inițializare pin pentru modulul de detecție a sunetului
  pinMode(soundSensorPin, INPUT);

  // Inițializare seminte pentru funcția random
  randomSeed(analogRead(0));
}

void loop() {
  // Citirea valorii de la modulul de detecție a sunetului
  int soundDetected = digitalRead(soundSensorPin);
  
  // Dacă se detectează sunet
  if (soundDetected == HIGH) {
    // Mâna dreaptă salută și mâna stângă mută obiect
    rightHandShake();
    leftHandMoveObject();
  }
}

// Funcție pentru a seta unghiul unui servomotor
void moveServo(int channel, int angle) {
  int pulseLength = map(angle, 0, 180, 150, 600); // Conversie unghi în puls
  pwm.setPWM(channel, 0, pulseLength);
}

// Funcție pentru a seta unghiul unui servomotor lent
void moveServoSlowly(int channel, int startAngle, int endAngle, int stepDelay) {
  if (startAngle < endAngle) {
    for (int angle = startAngle; angle <= endAngle; angle++) {
      moveServo(channel, angle);
      delay(stepDelay);
    }
  } else {
    for (int angle = startAngle; angle >= endAngle; angle--) {
      moveServo(channel, angle);
      delay(stepDelay);
    }
  }
}

// Funcție pentru salutul mâinii drepte
void rightHandShake() {
  // Ridicare braț drept pentru salut
  moveServoSlowly(channelServoDreaptaUmarX, 0, 90, 20);
  moveServoSlowly(channelServoDreaptaCot, 0, 90, 20);
  moveServoSlowly(channelServoDreaptaAntebrat, 0, 70, 20);
  delay(500); // Așteaptă 0.5 secunde
  
  // Mișcări de salut
  for (int i = 0; i < 3; i++) {
    moveServoSlowly(channelServoDreaptaCot, 0, 45, 20);
    moveServoSlowly(channelServoDreaptaCot, 45, 0, 20);
  }
  
  // Resetare la poziția inițială
  moveServoSlowly(channelServoDreaptaCot, 0, 100, 20);
  moveServoSlowly(channelServoDreaptaUmarX, 90, 0, 20);
}

// Funcție pentru mișcarea obiectului de mâna stângă
void leftHandMoveObject() {
  // Ridicare braț stâng pentru a lua obiectul
  moveServoSlowly(channelServoStangaUmarX, 0, 15, 20);
  moveServoSlowly(channelServoStangaCot, 0, 90, 20);
  moveServoSlowly(channelServoStangaAntebrat, 0, 45, 20);
  delay(500); // Așteaptă 0.5 secunde
  
  // Închidere degete pentru a prinde obiectul (toate deodată)
  closeLeftHand();
  delay(500); // Așteaptă 0.5 secunde
  
  // Mutare obiect către stânga
  moveServoSlowly(channelServoStangaUmarX, 60, 135, 20);
  delay(500); // Așteaptă 0.5 secunde
  
  // Deschidere degete pentru a elibera obiectul (toate deodată)
  openLeftHand();
  delay(500); // Așteaptă 0.5 secunde
  
  // Resetare la poziția inițială
  moveServoSlowly(channelServoStangaUmarX, 135, 0, 20);
  moveServoSlowly(channelServoStangaCot, 90, 0, 20);
  moveServoSlowly(channelServoStangaAntebrat, 45, 0, 20);
}

// Funcție pentru a deschide toate degetele mâinii stângi
void closeLeftHand() {
  moveServoSlowly(channelServoStangaDeget1, 90, 0, 20);
  moveServoSlowly(channelServoStangaDeget2, 90, 0, 20);
  moveServoSlowly(channelServoStangaDeget3, 90, 0, 20);
  moveServoSlowly(channelServoStangaDeget4, 90, 0, 20);
  moveServoSlowly(channelServoStangaDeget5, 90, 0, 20);
}

// Funcție pentru a inchide toate degetele mâinii stângi
void openLeftHand() {
  moveServoSlowly(channelServoStangaDeget1, 0, 90, 20);
  moveServoSlowly(channelServoStangaDeget2, 0, 90, 20);
  moveServoSlowly(channelServoStangaDeget3, 0, 90, 20);
  moveServoSlowly(channelServoStangaDeget4, 0, 90, 20);
  moveServoSlowly(channelServoStangaDeget5, 0, 90, 20);

}





