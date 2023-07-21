#include <Servo.h>

const int trigPin = 2;    // 초음파 센서의 Trig 핀
const int echoPin = 3;    // 초음파 센서의 Echo 핀
const int servoPin = 9;   // 서보 모터의 핀

Servo myservo;
int distanceThreshold = 15;  // 동작을 수행할 거리 임계값 (15 이하일 때 동작)
int angle = 120;
int scale;
int serialCount = 0;
int data = 0;

void setup() {
  scale = 0;
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  myservo.attach(servoPin);
  myservo.write(120);  // 서보 모터의 초기 위치 설정
  Serial.begin(115200);
}

void loop() {
  
  long duration, distance;
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  duration = pulseIn(echoPin, HIGH);
  distance = duration * 17 / 1000;
  
  if(Serial.available()>0) {
    if (serialCount == 0){
      data = Serial.parseInt();
      serialCount++;
    }
    if (serialCount == 1){
      scale = Serial.parseInt();
    }
  }
  if (data == 1) {
    if (scale == 3) {
      if (distance <= distanceThreshold) {
        delay(4000);
        while (angle > 0 && angle <= 180) {
          Serial.print("angle1");
          Serial.println(angle);
          
          myservo.write(angle);
          angle=angle-1;
          delay(5);
          if (angle == 80){
            angle = 120;
            myservo.write(angle);
            delay(6000);
            break;
          }
        }  
      }
    }
  }
  if (data == 2){
      if (scale == 3){
        if (distance <= distanceThreshold) {
          delay(4000);
          while (angle > 0 && angle <= 180){
          Serial.print("angle2");
          Serial.println(angle);
          
          myservo.write(angle);
          angle=angle-1;
          delay(5);
          if (angle == 30){
            angle = 120;
            myservo.write(angle);
            delay(6000);
            break;
          }
        }  
      }
    }  
  }
  Serial.print("data: ");
  Serial.println(data);
  Serial.print("scale: ");
  Serial.println(scale);
  Serial.print("angle: ");
  Serial.println(angle);
  Serial.print("distance: ");
  Serial.println(distance);
  
  delay(100);  // 다음 측정까지의 지연 시간 (0.1초)
  }