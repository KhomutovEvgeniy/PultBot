""" Конфигурация робота """
from RPiPWM import *
"""
    F - Front
    B - Backside
    L - Left
    R - Right
"""
IP = '173.1.0.92'  # IP адрес куда отправляем видео

chanSrvFL = 1   # канал для передней левой сервы
chanSvrFR = 2   # канал для передней правой сервы
chanSrvBL = 3   # канал для задней левой сервы
chanSrvBR = 4   # канал для задней правой сервы
chanSvrCAM = 5  # канал для сервы с камерой

chanRevMotorLB = 12     # каналы моторов, индексы аналогичны сервам
chanRevMotorRB = 13

SvrFL = Servo90(chanSrvFL)  # передняя левая
SvrFLResolution = (0, 90)   # разрешение

SvrFR = Servo90(chanSvrFR)  # передняя правая
SvrFRResolution = (0, 90)   # разрешение

SvrBL = Servo90(chanSrvBL)  # задняя левая
SvrBLResolution = (0, 90)   # разрешение

SvrBR = Servo90(chanSrvBR)  # задняя правая
SvrBRResolution = (0, 90)   # разрешение

SvrCAM = Servo90(chanSvrCAM)    # серва с камерой
SvrCaMResolution = (0, 90)

MotorLB = ReverseMotor(chanRevMotorLB)  # моторы, индексы аналогичные
MotorRB = ReverseMotor(chanRevMotorRB)


RPCServerPort = 8000    # порт RPC сервера
