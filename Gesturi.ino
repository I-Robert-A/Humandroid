COD PENTRU GESTICULARE ROBOT
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
    // Exemplu de mișcări de gesticulare
    gesticulate();
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

// Funcție pentru mișcări de gesticulare
void gesticulate() {
  // Mișcare 1
  moveServoSlowly(channelServoStangaUmarX, 0, 45, 20);
  moveServoSlowly(channelServoDreaptaUmarX, 0, 135, 20);
  delay(500); // Așteaptă 0.5 secunde
  
  // Mișcare 2
  moveServoSlowly(channelServoStangaCot, 0, 90, 20);
  moveServoSlowly(channelServoDreaptaCot, 0, 90, 20);
  delay(500); // Așteaptă 0.5 secunde
  
  // Mișcare 3
  moveServoSlowly(channelServoStangaAntebrat, 0, 45, 20);
  moveServoSlowly(channelServoDreaptaAntebrat, 0, 135, 20);
  delay(500); // Așteaptă 0.5 secunde

  // Mișcări aleatorii ale degetelor
  moveServoSlowly(channelServoStangaDeget1, 0, random(0, 180), 20);
  moveServoSlowly(channelServoStangaDeget2, 0, random(0, 180), 20);
  moveServoSlowly(channelServoStangaDeget3, 0, random(0, 180), 20);
  moveServoSlowly(channelServoStangaDeget4, 0, random(0, 180), 20);
  moveServoSlowly(channelServoStangaDeget5, 0, random(0, 180), 20);
  delay(500); // Așteaptă 0.5 secunde
  
  // Resetare la poziția inițială
  moveServoSlowly(channelServoStangaUmarX, 45, 0, 20);
  moveServoSlowly(channelServoDreaptaUmarX, 135, 0, 20);
  moveServoSlowly(channelServoStangaCot, 90, 0, 20);
  moveServoSlowly(channelServoDreaptaCot, 90, 0, 20);
  moveServoSlowly(channelServoStangaAntebrat, 45, 0, 20);
  moveServoSlowly(channelServoDreaptaAntebrat, 135, 0, 20);
  moveServoSlowly(channelServoStangaDeget1, 180, 0, 20);
  moveServoSlowly(channelServoStangaDeget2, 180, 0, 20);
  moveServoSlowly(channelServoStangaDeget3, 180, 0, 20);
  moveServoSlowly(channelServoStangaDeget4, 180, 0, 20);
  moveServoSlowly(channelServoStangaDeget5, 180, 0, 20);
  delay(500); // Așteaptă 0.5 secunde
}
