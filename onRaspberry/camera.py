#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import cv2
import numpy as np
import psutil
import threading
from config import *
import rpicam

from config import *

# настройки видеопотока
FORMAT = rpicam.FORMAT_H264  # поток H264
# FORMAT = rpicam.FORMAT_MJPG #поток MJPG
WIDTH, HEIGHT = 640, 360
RESOLUTION = (WIDTH, HEIGHT)
FRAMERATE = 30

# сетевые параметры

RTP_PORT = 5000  # порт отправки RTP видео

AUTO = False
SENSIVITY = 102
EXIT = False


def exit():
    global EXIT
    EXIT = True
    # останавливаем обработку кадров
    try:
        frameHandlerThread.stop()

        # останов трансляции c камеры
        rpiCamStreamer.stop()
        rpiCamStreamer.close()
    except:
        pass


def setAUTO(b):
    global AUTO
    AUTO = b


class FrameHandler(threading.Thread):
    def __init__(self, stream, setSpeed):
        super(FrameHandler, self).__init__()
        self.middle = 106
        self.frameWidth = 4 * int(640 / 6) + 15 - (2 * int(640 / 6) - 15)
        self.controlRate = 15
        self.setSpeed = setSpeed
        self.daemon = True
        self.rpiCamStream = stream
        self._frame = None
        self._frameCount = 0
        self._stopped = threading.Event()  # событие для остановки потока
        self._newFrameEvent = threading.Event()  # событие для контроля поступления кадров

    def run(self):
        global AUTO  # инициализируем глобальные перменные
        while not self._stopped.is_set():  # пока мы живём
            while AUTO:  # если врублена автономка
                height = 480  # инициализируем размер фрейма
                width = 640
                self.rpiCamStream.frameRequest()  # отправил запрос на новый кадр
                self._newFrameEvent.wait()  # ждем появления нового кадра
                if not (self._frame is None):  # если кадр есть
                    frame = self._frame[4 * int(height / 5):height,
                            2 * int(width / 6) - 15:4 * int(width / 6) + 15]  # обрезаем для оценки инверсности
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # делаем ч/б

                    intensivity = int(gray.mean())  # получаем среднее значение
                    if intensivity < 135:  # условие интесивности
                        ret, binary = cv2.threshold(gray, SENSIVITY, 255,
                                                    cv2.THRESH_BINARY)  # если инверсная инвертируем картинку
                    else:
                        ret, binary = cv2.threshold(gray, SENSIVITY, 255,
                                                    cv2.THRESH_BINARY_INV)  # переводим в ьинарное изображение
                    # Find the contours of the frame
                    cont_img, contours, hierarchy = cv2.findContours(binary.copy(), 1,
                                                                     cv2.CHAIN_APPROX_NONE)  # получаем список контуров

                    # Find the biggest contour (if detected)
                    if len(contours) > 0:  # если нашли контур
                        c = max(contours, key=cv2.contourArea)  # ищем максимальный контур
                        M = cv2.moments(c)  # получаем массив с координатами
                        if M['m00'] != 0:
                            cx = int(M['m10'] / M['m00'])  # координата центра по х
                            cy = int(M['m01'] / M['m00'])  # координата центра по у
                        cv2.line(frame, (cx, 0), (cx, height), (255, 0, 0), 1)  # рисуем линни
                        cv2.line(frame, (0, cy), (width, cy), (255, 0, 0), 1)

                        cv2.drawContours(frame, contours, -1, (0, 255, 0), 1)  # рисуем контур
                        self.sender.addFrame(frame)

                        speed = 55

                        diff = cx / (self.frameWidth / 2) - 1
                        if cy > 80:
                            diff *= 25

                        leftSpeed = int(speed + diff * self.controlRate)
                        rightSpeed = int(speed - diff * self.controlRate)
                        print('Left: %s Right: %s' % (leftSpeed, rightSpeed))
                        self.setSpeed(-leftSpeed, -rightSpeed, True)

                    else:  # если не нашли контур
                        print("I don't see the line")
                        self.setSpeed(0, 0)

                self._newFrameEvent.clear()  # сбрасываем событие

        print('Frame handler stopped')
        self.setSpeed(0, 0)

    def stop(self):  # остановка потока
        self._stopped.set()
        if not self._newFrameEvent.is_set():  # если кадр не обрабатывается
            self._frame = None
            self._newFrameEvent.set()
        self.join()

    def setFrame(self, frame):  # задание нового кадра для обработки
        if not self._newFrameEvent.is_set():  # если обработчик готов принять новый кадр
            self._frame = frame
            self._newFrameEvent.set()  # задали событие
        return self._newFrameEvent.is_set()


def onFrameCallback(frame):  # обработчик события 'получен кадр'
    # print('New frame')
    frameHandlerThread.setFrame(frame)  # задали новый кадр


# проверка наличия камеры в системе
assert rpicam.checkCamera(), 'Raspberry Pi camera not found'

# создаем трансляцию с камеры (тип потока h264/mjpeg, разрешение, частота кадров, хост куда шлем, функция обрабтчик
# кадров)
rpiCamStreamer = rpicam.RPiCamStreamer(FORMAT, RESOLUTION, FRAMERATE, (IP, RTP_PORT), onFrameCallback)
# robotCamStreamer.setFlip(False, True) #отражаем кадр (вертикальное отражение, горизонтальное отражение)
rpiCamStreamer.setRotation(180)  # поворачиваем кадр на 180 град, доступные значения 90, 180, 270


def setSpeed(l, r):
    SvrFL.SetValue(l)
    SvrBL.SetValue(l)

    SvrFR.SetValue(r)
    SvrBR.SetValue(r)


# поток обработки кадров
frameHandlerThread = FrameHandler(rpiCamStreamer, setSpeed)

