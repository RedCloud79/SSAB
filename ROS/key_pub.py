#!/usr/bin/env python
# -*- coding : utf-8 -*-

import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import String
import sys, select, termios, tty
import socket
import time
import signal
import os

def signal_handler(sig, frame):
    print("Terminated")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

msgStart = """
Control Your Robot!
---------------------------
Moving around:
   w
a  s  d
   x

w/x : increase/decrease linear velocity
a/d : increase/decrease angular velocity
space key, s : stop
anything else : stop and exit
"""

def getKey():
    tty.setraw(sys.stdin.fileno())
    select.select([sys.stdin], [], [], 0)
    key = sys.stdin.read(1)
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

##############################################

speed = 0.0
turn = 0.0
lineCodeInfo = None
qrCodeInfo = None
lineDriveTrigger = False
qrStopTrigger = False

##############################################

def vels(speed, turn):
    return "currently:\tspeed %s\tturn %s " % (speed, turn)

def qrCodeInfoCallback(msg):
    global qrCodeInfo
    global qrStopTrigger
    qrCodeInfo = msg.data
    print("qrCodeInfo: " + qrCodeInfo)
    qrStopTrigger = True

def lineCodeInfoCallback(msg):
    global lineCodeInfo
    global lineDriveTrigger
    lineCodeInfo = msg.data
    print("lineCodeInfo: " + lineCodeInfo)
    lineDriveTrigger = True

def lineCodeDrive():
    global lineDriveTrigger
    
    if lineCodeInfo == "L":
        speed = 0.2
        turn = 1.0
        print(vels(speed, turn))
        twist = Twist()
        twist.linear.x = speed
        twist.angular.z = turn
        pub.publish(twist)
    elif lineCodeInfo == "R":
        speed = 0.2
        turn = -1.0
        print(vels(speed, turn))
        twist = Twist()
        twist.linear.x = speed
        twist.angular.z = turn
        pub.publish(twist)
    elif lineCodeInfo == "F":
        speed = 0.28
        turn = 0.0
        print(vels(speed, turn))
        twist = Twist()
        twist.linear.x = speed
        twist.angular.z = turn
        pub.publish(twist)

    lineDriveTrigger = False

def qrCodeStop():

    global qrStopTrigger

    if qrCodeInfo == "Stop":
        speed = 0.0
        turn = 0.0
        print(vels(speed, turn))
        twist = Twist()
        twist.linear.x = speed
        twist.angular.z = turn
        pub.publish(twist)
        time.sleep(10)

    qrStopTrigger = False

def keyboardControl(msg):
    status = 0
    try:
        print(msgStart)
        print(vels(speed, turn))
        while(1):
            if msg == "start":
                key = getKey()
                if key in ['w', 'W']:
                    speed = 0.5
                    turn = 0.0
                    print(vels(speed, turn))
                elif key in ['x', 'X']:
                    speed = -0.5
                    turn = 0.0
                    print(vels(speed, turn))
                elif key in ['a', 'A']:
                    speed = 0.0
                    turn = + 3.5
                    print(vels(speed, turn))
                elif key in ['d', 'D']:
                    speed = 0.0
                    turn = -3.5
                    print(vels(speed, turn))
                elif key in [' ', 's', 'S']:
                    speed = 0.0
                    turn = 0.0
                    print(vels(speed, turn))
                else:
                    if key == '\x03':
                        break

                twist = Twist()
                twist.linear.x = speed
                twist.angular.z = turn
                pub.publish(twist)

    except Exception as e:
        print(e)

    finally:
        twist = Twist()
        twist.linear.x = 0
        twist.angular.z = 0
        pub.publish(twist)

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)

if __name__=="__main__":

    ##################################################
    
    # socket creation
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # IP address & PORT address
    ip = "192.168.0.70"
    port = 12333

    # binging socket ip & port
    sock.bind((ip, port))

    settings = termios.tcgetattr(sys.stdin)

    rospy.init_node('teleop_twist_keyboard')

    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    info_sub1 = rospy.Subscriber('/qr_code_info', String, qrCodeInfoCallback)
    info_sub2 = rospy.Subscriber('/line_code_info', String, lineCodeInfoCallback)

    ##################################################

    # wait socket
    print("Waiting......")
    sock.listen(1)
    try:
        while True:
            # Publisher connect
            conn, addr = sock.accept()

            # data receive
            socketMsg = conn.recv(1024).decode()

            if socketMsg:
                print("Received: " + socketMsg)
                break

    except KeyboardInterrupt:
        print('terminated.')

    ##################################################

    socketMsg = "start"

    if socketMsg == "start":
        print("Driving Start")
        while True:
            if lineDriveTrigger == True:
                lineCodeDrive()
            if qrStopTrigger == True:
                qrCodeStop()

    os._exit()

os._exit()

    ##################################################
