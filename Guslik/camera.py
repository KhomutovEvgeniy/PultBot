#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import cv2
import numpy as np
import psutil
import threading
import rpicam
import config

# настройки видеопотока
# FORMAT = rpicam.FORMAT_H264  # поток H264
FORMAT = rpicam.FORMAT_MJPEG  # поток MJPEG
WIDTH, HEIGHT = 640, 360
RESOLUTION = (WIDTH, HEIGHT)
FRAMERATE = 30


class FrameHandler(threading.Thread):

    def __init__(self, stream):
        super(FrameHandler, self).__init__()
        self.middle = 106
        self._cvFrameRect = 105, 70, 430, 200  # прямоугольник, выделяемый в кадре для OpenCV: x, y, width, height
        self.speed = 25
        self.daemon = True
        self.rpiCamStream = stream
        self._frame = None
        self._frameCount = 0
        self._stopped = threading.Event()  # событие для остановки потока
        self._newFrameEvent = threading.Event()  # событие для контроля поступления кадров

    def run(self):
        print('Frame handler started')
        while not self._stopped.is_set():  # пока мы живём
            while config.AUTO:  # если врублена автономка
                self.rpiCamStream.frameRequest()  # отправил запрос на новый кадр
                self._newFrameEvent.wait()  # ждем появления нового кадра
                if not (self._frame is None):  # если кадр есть
                    r = self._cvFrameRect
                    frame = self._frame[r[1]:r[1]+r[3], r[0]:r[0]+r[2]]   # r - прямоугольник: x, y, width, height
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # делаем ч/б

                    intensivity = int(gray.mean())  # получаем среднее значение
                    if intensivity < 135:  # условие интесивности
                        ret, binary = cv2.threshold(gray, config.SENSIVITY, 255,
                                                    cv2.THRESH_BINARY)  # если инверсная инвертируем картинку
                        print("Inverse")
                    else:
                        ret, binary = cv2.threshold(gray, config.SENSIVITY, 255,
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
                        cv2.line(frame, (cx, 0), (cx, r[3]), (255, 0, 0), 1)  # рисуем линни
                        cv2.line(frame, (0, cy), (r[2], cy), (255, 0, 0), 1)

                        cv2.drawContours(frame, contours, -1, (0, 255, 0), 1)  # рисуем контур

                        diff = cx / (r[2] / 2) - 1

                        config.turnForward(diff)
                        config.move(self.speed)

                    else:  # если не нашли контур
                        print("I don't see the line")
                        config.move(0)

                self._newFrameEvent.clear()  # сбрасываем событие
            time.sleep(0.1)
        print('Frame handler stopped')
        config.move(0)

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
    frameHandlerThread.setFrame(frame)  # задали новый кадр


# проверка наличия камеры в системе
assert rpicam.checkCamera(), 'Raspberry Pi camera not found'

# создаем трансляцию с камеры (тип потока h264/mjpeg, разрешение, частота кадров, хост куда шлем, функция обрабтчик
# кадров)
rpiCamStreamer = rpicam.RPiCamStreamer(FORMAT, RESOLUTION, FRAMERATE, (config.IP, config.RTP_PORT), onFrameCallback)
# robotCamStreamer.setFlip(False, True) #отражаем кадр (вертикальное отражение, горизонтальное отражение)
rpiCamStreamer.setRotation(180)  # поворачиваем кадр на 180 град, доступные значения 90, 180, 270

# поток обработки кадров
frameHandlerThread = FrameHandler(rpiCamStreamer)


def start():
    rpiCamStreamer.start()  # запускаем трансляцию
    frameHandlerThread.start()  # запускаем обработку
