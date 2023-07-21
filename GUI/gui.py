from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

import sys
from std_msgs.msg import String

import socket

import signal

def signal_handler(sig, frame):
    print("Terminated")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Vending Machine
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Subscriber IP & Port
subscriber_ip = "192.168.0.71"
subscriber_port = 12345

# Robot
sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Subscriber IP & Port
subscriber2_ip = "192.168.0.70"
subscriber2_port = 12333

class MainWindow(QWidget):
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

        self.itemInfo = QLabel(self)
        self.itemInfo.setText("Default")
        self.itemInfo.setFixedSize(150,50)
        self.itemInfo.setAlignment(Qt.AlignCenter)
        
        itemNameLayout = QHBoxLayout()
        itemNameLayout.addWidget(self.itemText)
        itemNameLayout.addWidget(self.itemInfo)

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

        itemQuantityLayout = QHBoxLayout()
        itemQuantityLayout.addWidget(self.itemQuantityText)
        itemQuantityLayout.addWidget(self.itemQuantityTextEdit)
        itemQuantityLayout.addWidget(self.itemQuantityButton)

        self.finalText = QLabel(self)
        self.finalText.setText("최종 : ")
        self.finalText.setFixedSize(50,50)

        self.finalInfo = QLabel(self)
        self.finalInfo.setText("Default")
        self.finalInfo.setFixedSize(150,50)

        finalLayout = QHBoxLayout()
        finalLayout.addWidget(self.finalText)
        finalLayout.addWidget(self.finalInfo)

        itemInfoLayout = QVBoxLayout()
        itemInfoLayout.addLayout(itemNameLayout)
        itemInfoLayout.addLayout(itemQuantityLayout)
        itemInfoLayout.addLayout(finalLayout)

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

        imageLayout = QHBoxLayout()
        imageLayout.addWidget(self.button1)
        imageLayout.addWidget(self.button2)
        imageLayout.addWidget(self.button3)

        runButtonLayout = QVBoxLayout()
        runButtonLayout.addWidget(self.runButton1)
        runButtonLayout.addWidget(self.runButton2)
        
        itemAndButtonLayout = QHBoxLayout()
        itemAndButtonLayout.addLayout(itemInfoLayout)
        itemAndButtonLayout.addLayout(runButtonLayout)    
        
        layout = QVBoxLayout()
        layout.addLayout(imageLayout)
        layout.addLayout(itemAndButtonLayout)
        
        self.on_button1_clicked()

        self.setLayout(layout)

    def on_button1_clicked(self):
        self.itemInfo.setText("Marlboro")
        self.itemName = "Marlboro"
        self.itemQuantityTextEdit.setText("")
        self.finalInfo.setText("")

    def on_button2_clicked(self):
        self.itemInfo.setText("IceVolt")
        self.itemName = "IceVolt"
        self.itemQuantityTextEdit.setText("")
        self.finalInfo.setText("")

    def on_button3_clicked(self):
        self.itemInfo.setText("FrenchBlack")
        self.itemName = "FrenchBlack"
        self.itemQuantityTextEdit.setText("")
        self.finalInfo.setText("")

    def on_runButton1_clicked(self):
        # vendingMachine
        data = self.itemQuantity
        print(data)
        sock.connect((subscriber_ip, subscriber_port))
        sock.sendall(data.encode())
        sock.close()

    def on_runButton2_clicked(self):
        # Robot
        msg = "start"
        sock2.connect((subscriber2_ip, subscriber2_port))
        sock2.sendall(msg.encode())
        sock2.close()
    
    def on_quantity_clicked(self):
        self.itemQuantity = self.itemQuantityTextEdit.toPlainText()
        self.finalInfo.setText(self.itemName + " " + self.itemQuantity + "개")
        
        

def prepare():
    # rospy.init_node('gui')
    pass
    
if __name__ == '__main__':

    prepare()

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec_()
