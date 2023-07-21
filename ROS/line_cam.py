#!/usr/bin/env python

import numpy as np
import cv2
import rospy
from std_msgs.msg import String
import signal
import sys

def signal_handler(sig, frame):
    print("Terminated")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)


cap = cv2.VideoCapture(0)

rospy.init_node('line_cam')

info_pub = rospy.Publisher('/line_code_info', String, queue_size=10)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (1280, 720))
    snip = frame[600:720, :]

    # Threshold -> Only Black Line
    gray = cv2.cvtColor(snip, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 90, 255, cv2.THRESH_BINARY)

    # Noise Canceling
    kernel = np.ones((5, 5), np.uint8)
    thresh = cv2.dilate(thresh, kernel, iterations=1)

    # Edge Detection
    edges = cv2.Canny(thresh, 50, 150)

    lines = cv2.HoughLines(edges, 1, np.pi / 180, 100)

    left_lines = []
    right_lines = []

    if lines is not None:
        for line in lines:
            rho, theta = line[0]
            if theta < np.pi / 2:
                left_lines.append((rho, theta))
            else:
                right_lines.append((rho, theta))

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

    if len(right_lines) > 0:
        right_rho, right_theta = np.median(right_lines, axis=0)
        a = np.cos(right_theta)
        b = np.sin(right_theta)
        x0 = a * right_rho
        y0 = b * right_rho
        x1 = int(x0 + 400 * (-b))
        y1 = int(y0 + 400 * (a))
        x2 = int(x0 - 600 * (-b))
        y2 = int(y0 - 600 * (a))
        cv2.line(snip, (x1, y1), (x2, y2), (255, 0, 0), 2)
        cv2.putText(snip, 'Right line', (x2, y2), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    # Find the contour
    _, contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Find the contour with the approximate center
    center_contour = None
    min_distance = float('inf')
    for contour in contours:
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            distance = abs(cX - snip.shape[1] // 2)
            if distance < min_distance:
                center_contour = contour
                min_distance = distance

    # Draw the center contour
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

            #loop_rate = rospy.Rate(10)

            info_pub.publish(info_msg)

            #loop_rate.sleep()

            cv2.putText(snip, 'info_msg:' + info_msg , (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    cv2.imshow("Lane Detection", snip)

    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
