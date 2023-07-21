# GUI ( 화면 구성 )

## 구성 및 동작 설명
<img width="100%" alt="GUI 화면" src="https://github.com/RedCloud79/SSAB/blob/main/GUI/GUI%ED%99%94%EB%A9%B4.png" />

#### 구성
> * 상품을 표기해주는 이미지란 Button형식으로 구성
>   
> * 해당 상품을 선택을 했을 경우 상품명 출력
>   
> * 상품의 수량을 기입후 입력의 경우 **최종**란에 상품명 및 수량 표기
>   
> * **정보 장판기로 전송**의 경우 socket 통신에 의한 수량값 전달
>   
> * **로봇 Start**의 버튼 동작시 socket 통신에 의한 'start'값 전달


#### 코드 구성
> * PySide2를 활용한 GUI구성


<details>
  <summarty> GUI 구성 코드 </summarty>

  ```python
def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.button1 = QPushButton(self)
        self.button1.setIcon(QIcon("./res/Marlboro.jpg"))
        self.button1.setIconSize(QSize(200,200))
        self.button1.clicked.connect(self.on_button1_clicked)

        self.button2 = QPushButton(self)
        self.button2.setIcon(QIcon("./res/IceVolt.jpg"))
        self.button2.setIconSize(QSize(200,200))
        self.button2.clicked.connect(self.on_button2_clicked)

        self.button3 = QPushButton(self)
        self.button3.setIcon(QIcon("./res/Mevius.jpg"))
        self.button3.setIconSize(QSize(200,200))
        self.button3.clicked.connect(self.on_button3_clicked)

        self.itemText = QLabel(self)
        self.itemText.setText("상품명 : ")
        self.itemText.setFixedSize(50,50)
        self.itemText.setAlignment(Qt.AlignCenter)

        self.itemQuantityText = QLabel(self)
        self.itemQuantityText.setText("수량 : ")
        self.itemQuantityText.setFixedSize(50,50)
        self.itemQuantityText.setAlignment(Qt.AlignCenter)

        self.itemQuantityTextEdit = QTextEdit()
        self.itemQuantityTextEdit.setFixedSize(100,50)

        self.itemQuantityButton = QPushButton()
        self.itemQuantityButton.setText("입력")
        self.itemQuantityButton.setFixedSize(50,50)
        self.itemQuantityButton.clicked.connect(self.on_quantity_clicked)

        self.finalText = QLabel(self)
        self.finalText.setText("최종 : ")
        self.finalText.setFixedSize(50,50)

        self.runButton1 = QPushButton("정보 자판기로 전송", self)
        self.runButton1.setFixedSize(180,50)
        font1 = self.runButton1.font()
        font1.setPointSize(14)
        self.runButton1.setFont(font1)
        self.runButton1.clicked.connect(self.on_runButton1_clicked)

        self.runButton2 = QPushButton("로봇 START", self)
        self.runButton2.setFixedSize(180,50)
        font2 = self.runButton2.font()
        font2.setPointSize(16)
        self.runButton2.setFont(font2)
        self.runButton2.clicked.connect(self.on_runButton2_clicked)
  ```
  
</details>



> * socket 통신을 활용한 Vending_machine와 ROS의 연결   
```python
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Subscriber IP & Port
subscriber_ip = "192.168.0.(고유 ip입력)"
subscriber_port = 12345
```

> * 전송 버튼에 대한 동작
```python
self.runButton1 = QPushButton("정보 자판기로 전송", self)
        self.runButton1.setFixedSize(180,50)
        font1 = self.runButton1.font()
        font1.setPointSize(14)
        self.runButton1.setFont(font1)
        self.runButton1.clicked.connect(self.on_runButton1_clicked)
```

> * 전송 버튼에 대한 동작이 들어왔을 경우 동작하는 함수
```python
def on_runButton1_clicked(self):
        # vendingMachine
        data = self.itemQuantity
        print(data)
        sock.connect((subscriber_ip, subscriber_port))
        sock.sendall(data.encode())
        sock.close()
```













