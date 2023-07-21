import cv2
import numpy as np
from skimage.transform import resize
import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow import keras
import RPi.GPIO as GPIO
import time
import serial
import socket
servo_pin = 2

GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin, GPIO.OUT)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# ip Adress
ip = "192.168.0.71"
port = 12345

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
try:
    print("Waiting......")
    while True:
        
        conn, addr = sock.accept()

        quantity = conn.recv(1024).decode()

        print(quantity)

        ser.write(quantity.encode())

        break

except KeyboardInterrupt:
    print("Terminated")

conn.close()
sock.close()

# 학습된 모델을 LOAD
model = keras.models.load_model('my_model.h5')
model.summary()

scale = 0

drawing = False  # True is Mouse Click
ix, iy = -1, -1

# Mouse Callback
def draw_circle(event, x, y, flags, param):
    global ix, iy, drawing

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y

    if event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            cv2.circle(img, (x, y), 5, (255, 255, 255), -1)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        cv2.circle(img, (x, y), 5, (255, 255, 255), -1)

trigger = True

def answer(img):
    
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

    for contour in selected_contours:
        x, y, w, h = cv2.boundingRect(contour)
        contour_center_x = x + (w // 2)
        contour_center_y = y + (h // 2)

        # 웹캠 영상 중앙에 위치한 숫자만 인식
        if abs(contour_center_x - img_center_x) < img.shape[1] // 4 and abs(contour_center_y - img_center_y) < img.shape[0] // 4:
            digit_img = img_threshold[y:y+h, x:x+w]
            digit_img = cv2.resize(digit_img, (28, 28), interpolation=cv2.INTER_AREA)
            digit_img = digit_img.astype('float32') / 255.0
            digit_img = digit_img.reshape((1, 28, 28, 1))
            
            prediction = model.predict(digit_img)
            predicted_class = np.argmax(prediction)
            confidence = prediction[0][predicted_class] * 100
            
            # 학습된 숫자만 인식한 경우에만 결과를 표시
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


    cv2.imshow('image', img)
    cv2.imshow('test', img_threshold) 
# 웹캠 스트림 열기
cap = cv2.VideoCapture(0)

#degree = 70

#ser.write(degree)

# 창 생성 및 마우스 콜백 등록
#cv2.namedWindow('image')
#cv2.setMouseCallback('image', draw_circle)

while True:
    # 프레임 읽기
    ret, frame = cap.read()

    if not ret:
        print("Failed to capture frame from webcam")
        break

    # 화면에 표시할 이미지 복사
    img = frame.copy()

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

    # ROI 영역만 추출하여 숫자 인식 수행
    roi_img = img[roi_start_y:roi_end_y, roi_start_x:roi_end_x]
    answer(roi_img)

    print('scale', scale)
    #ser.write(scale)
    #cv2.imshow("roi_img", roi_img)

    # ESC 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == 27:
        break

# 리소스 해제
cap.release()
cv2.destroyAllWindows()
