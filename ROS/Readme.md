# ROS (구동 파트)
### 참고 pip, package
[ROS_PIP_LIST](ROS_pip_list.md)   
[ROS_PACKAGE_LIST](ROS_package_list.md)

## ROS_rqt_graph
<img width="100%" alt="GUI 화면" src="https://github.com/RedCloud79/SSAB/blob/main/ROS/ROS_rqt_graph.png" />

## ROS line_cam 구성
<img width="100%" alt="GUI 화면" src="https://github.com/RedCloud79/SSAB/blob/main/ROS/%EC%A0%84%EB%A9%B4%EB%B6%80%20%EC%B9%B4%EB%A9%94%EB%9D%BC%20%ED%99%94%EB%A9%B4.png" />

> * 전면부의 카메라를 통해 영상값을 불러옵니다.
```python
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (1280, 720))
    snip = frame[600:720, :]

    # Threshold -> Only Black Line
    gray = cv2.cvtColor(snip, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 90, 255, cv2.THRESH_BINARY)
```

> * BGR2GRAY와 THRESH_BINARY를 통해서 라인을 검출하는 동작을 수행합니다.
> * 좌표에 의해 좌측, 우측의 line을 인식합니다.
```python
if len(left_lines) > 0:
        left_rho, left_theta = np.median(left_lines, axis=0)
        a = np.cos(left_theta)
        b = np.sin(left_theta)
        x0 = a * left_rho
        y0 = b * left_rho
        x1 = int(x0 + 400 * (-b))
        y1 = int(y0 + 400 * (a))
        x2 = int(x0 - 600 * (-b))
        y2 = int(y0 - 600 * (a))
        cv2.line(snip, (x1, y1), (x2, y2), (0, 0, 255), 2)
        cv2.putText(snip, 'Left line', (x2, y2), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
```


> * line을 인식하여 좌,우측의 값사이의 공간을 contour를 통하여 중앙값을 Value로 L,R,F의 값을 판별 합니다.
```python
if center_contour is not None:
        cv2.drawContours(snip, [center_contour], -1, (0, 255, 0), 2)

        # Calculate the center coordinates
        M = cv2.moments(center_contour)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            cv2.circle(snip, (cX, cY), 5, (0, 255, 0), -1)
            # cv2.putText(snip, 'center x value:' + str(cX) , (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            # screen size : 1280x720    ->  1280x220

            snip_width = 1280
            snip_left_width = snip_width / 2 - 60
            snip_right_width = snip_width / 2 + 60

            if (cX < snip_left_width):
                info_msg = "L"
            elif (cX > snip_right_width):
                info_msg = "R"
            elif (cX >= snip_left_width and cX <= snip_right_width):
                info_msg = "F"
            else:
                info_msg = "Unknown"
```
> * 해당 출력값을 **info_pub = rospy.Publisher('/line_code_info', String, queue_size=10)**를 통해서 topic 통신으로 전달합니다.


## ROS Qr_cam 구성
> * Pyzbar라이브러리를 활용하여 바코드 혹은 Qr코드를 스캔하는 기능을 수행합니다.
> * 해당 결과값은 초기에 None값을 가지고 있고, topic 통신을 활용하여 값을 전달 수행을 합니다.
```python
allowed_formats = ['QRCODE', 'CODE128', 'EAN13']

rospy.init_node('qr_cam')

info_pub = rospy.Publisher('/qr_code_info', String, queue_size=10)

info_msg = None

```

> * 특정 Qr값에 url을 입력하여 동일한 url값이 입력받았을 경우 수행합니다.

```python
while True:
    ret, frame = cap.read()

    barcodes = pyzbar.decode(frame)

    for barcode in barcodes:
        barcode_type = barcode.type

        if barcode_type in allowed_formats:
            qr_code_data = barcode.data.decode("utf-8")

            if qr_code_data == 'http://m.site.naver.com/1aNhl':
                info_msg = "Stop"
            elif qr_code_data == 'http://m.site.naver.com/1aNl2':
                info_msg = "Stop"
            elif qr_code_data == 'https://m.sit.naver.com/1aN**':
                info_msg = "Daum"
            else:
                info_msg = "Unknown"
```

## ROS teleop_keyboard 구성
> * 이동체의 움직임을 주기위해 구성 되어있는 코드입니다.
> * Geometry_msgs를 활용하여 /cmd_vel토픽으로 값을 전송하여 속도를 제어합니다.
> * Cam에서 보내주는 topic들을 subscriber로 받아와 동작을 수행합니다.
```python
    rospy.init_node('teleop_twist_keyboard')

    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    info_sub1 = rospy.Subscriber('/qr_code_info', String, qrCodeInfoCallback)
    info_sub2 = rospy.Subscriber('/line_code_info', String, lineCodeInfoCallback)
```

> * 특정 topic값이 들어오면 speed는 앞or 뒤, turn 좌or 우의 값을 전달하여 Mobile의 움직임을 줍니다.
```python
if lineCodeInfo == "L":
        speed = 0.2
        turn = 1.0
        print(vels(speed, turn))
        twist = Twist()
        twist.linear.x = speed
        twist.angular.z = turn
        pub.publish(twist)
```

> * GUI에서 start라는 msgs값이 전달되면 이동체의 동작의 수행이 시작되게 해주었습니다.
```python
if socketMsg == "start":
        print("Driving Start")
        while True:
            if lineDriveTrigger == True:
                lineCodeDrive()
            if qrStopTrigger == True:
                qrCodeStop()

    os._exit()
```






