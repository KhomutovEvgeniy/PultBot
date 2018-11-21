#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from RTCJoystick import Joystick
from Control import Control
from config import *
import time
import GstCV
import cv2

joystick = Joystick()
joystick.connect("/dev/input/js0")
joystick.info()

control = Control()
control.setJoystick(joystick)
control.robot.connect(IP, PORT)

joystick.start()
control.start()
camera = GstCV.CVGstreamer(IP, 5000, 5001, 5005, toAVS=True, codec="JPEG")
camera.start()

SENSIVITY = 108     # чувствительность автономки
INTENSIVITY = 110   # порог интенсивности
r = 40, 70, 560, 200

while True:
    if camera.cvImage is not None:
        #print(camera.cvImage.shape)
        frame = camera.cvImage[r[1]:(r[1] + r[3]), r[0]:(r[0] + r[2])]  # r - прямоугольник: x, y, width, height
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        intensivity = int(gray.mean())
        if intensivity < 110:
            ret, binary = cv2.threshold(gray, SENSIVITY, 255, cv2.THRESH_BINARY)  # если инверсная инвертируем картинку
            print("Inverse")
        else:
            ret, binary = cv2.threshold(gray, SENSIVITY, 255,
                                        cv2.THRESH_BINARY_INV)  # переводим в ьинарное изображение
        cont_img, contours, hierarchy = cv2.findContours(binary, 1, cv2.CHAIN_APPROX_NONE)
        if len(contours) > 0:  # если нашли контур
            c = max(contours, key=cv2.contourArea)  # ищем максимальный контур
            M = cv2.moments(c)  # получаем массив с координатами
            if M['m00'] != 0:
                cx = int(M['m10'] / M['m00'])  # координата центра по х
                cy = int(M['m01'] / M['m00'])  # координата центра по у
            cv2.line(frame, (cx, 0), (cx, r[3]), (255, 0, 0), 1)  # рисуем линни
            cv2.line(frame, (0, cy), (r[2], cy), (255, 0, 0), 1)
            cv2.drawContours(frame, contours, -1, (0, 255, 0), 1)  # рисуем контур
            diff = cx / (r[2] / 2) - 1
            #print(diff)
        else:  # если не нашли контур
            print("I don't see the line")
            # move(0)
        cv2.imshow("YES", frame)
        cv2.imshow("NONE", camera.cvImage)
        cv2.imshow("bin", binary)
        cv2.imshow("gray", gray)
        cv2.waitKey(1)
    time.sleep(0.05)


