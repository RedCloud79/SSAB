# Vending_machine (구동 부분)

### 참고자료 pip
------------------------------------------------
[raspberrypi 4B pip list](/Vending_machine/Raspberry_pip_list.md)
------------------------------------------------

# 자판기 구성

<img width="100%" alt="GUI 화면" src="https://github.com/RedCloud79/SSAB/blob/main/Vending_machine/Vending_machine.PNG" />

## Arduino
> * 서보 모터와 초음파 센서를 활용하여 물건을 배출하는 기능을 가지고 있다.
> * 2, 3, 9번 핀을 활용 하였으며 라즈베리파이와의 통신을 위해 boardrate는 115200으로 설정을 해준다.
```C++
const int trigPin = 2;    // 초음파 센서의 Trig 핀
const int echoPin = 3;    // 초음파 센서의 Echo 핀
const int servoPin = 9;   // 서보 모터의 핀

void setup() {
  scale = 0;
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  myservo.attach(servoPin);
  myservo.write(120);  // 서보 모터의 초기 위치 설정
  Serial.begin(115200);
}
```

> * 시리얼 통신값을 받아서 동작을 하며, data, scale, distance의 값이 모두 일치하는 경우에 모터가 동작된다.
> * 모터의 각도를 1도씩 증가값을 주어 배출의 밀림 현상을 보완하여 작성되었다.
```C++
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
```

## Raspberry pi 4B
> * temsorflow라이브러리를 활용하여 객체를 구분하는 역할을 해준다.
> * socket을 활용하여 GUI의 와 연결 되어있으며, 숫자를 판별하기 위해서 MNIST모델을 활용하였다.
```python
ser = serial.Serial(
    port='/dev/ttyAMA1',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
    )


sock.bind((ip, port))

sock.listen()

# 학습된 모델을 LOAD
model = keras.models.load_model('my_model.h5')
model.summary()
```

> * 모델을 통해서 숫자를 인식하지만 무분별한 검출방지와 명확한 결과를 위해서 roi와 적응형 가우시안 스레시홀드를 적용시켰다.
> * 요츠 이진화 알고리즘은 그림자, 밝기에 따른 결과값의 차이가 있어서 적응형 가우시안을 활용하였다.
```python
global predicted_class, scale, trigger
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_gray = cv2.GaussianBlur(img_gray, (5, 5), 0)
    #_, img_threshold = cv2.threshold(img_gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    _, img_threshold = cv2.threshold(img_gray, 80, 255, cv2.THRESH_BINARY_INV)
    # 적응형 가우시안 스레시홀드 적용
    img_threshold = cv2.adaptiveThreshold(img_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 9, 5)
    contours, _ = cv2.findContours(img_threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    min_contour_size = 1000
    selected_contours = [cnt for cnt in contours if cv2.contourArea(cnt) >= min_contour_size]

    img_center_x = img.shape[1] // 2
    img_center_y = img.shape[0] // 2
```

> * 일정 확률 이상의 숫자만을 출력하게 하며 특정 값에 대해 일치하면 UART통신을 통한 시리얼값 전달의 동작이 수행된다.
```python
if confidence >= 85:
                cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(img, str(predicted_class), (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                cv2.putText(img, f'Confidence: {confidence:.2f}%', (x, y+h+25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                
                # 숫자를 인식한 경우에만 결과를 터미널에 출력
               # print('Predicted Digit:', predicted_class)
               # print('Confidence:', confidence, '%')
                scale = int(predicted_class)
                if scale == 3 and trigger == True:
                    scaleString = "3"
                    print(scaleString)
                    ser.write(scaleString.encode())
                    time.sleep(1.001)
                    trigger = False
                    break
```

> * 너무 넓은 화면각의 사용으로 인해서 fps에서 생기는 딜레이를 줄이기위해 roi설정을 통해서 속도를 올려주었다.
```python
# 웹캠 영상 중앙 좌표 계산
    img_center_x = img.shape[1] // 2
    img_center_y = img.shape[0] // 2

    # 웹캠 영상 중앙에 ROI를 설정
    roi_weight = 350
    roi_height = 450
    roi_start_x = img_center_x - (roi_weight // 2)
    roi_start_y = img_center_y - (roi_height // 2) 
    roi_end_x = roi_start_x + roi_weight
    roi_end_y = roi_start_y + roi_height

    # ROI 영역 표시
    cv2.rectangle(img, (roi_start_x, roi_start_y), (roi_end_x, roi_end_y), (255, 0, 0), 2)
```

















