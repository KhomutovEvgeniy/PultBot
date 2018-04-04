""" Конфигурация робота """
from onRaspberry.RPiPWM import *
"""
    F - Front
    B - Backside
    L - Left
    R - Right
"""
chanSrvFL = 1   # канал для передней левой сервы
chanSvrFR = 2   # канал для передней правой сервы
chanSrvBL = 3   # канал для задней левой сервы
chanSrvBR = 4   # канал для задней правой сервы

chanRevMotorFL = 12     # каналы моторов, индексы аналогичны сервам
chanRevMotorFR = 13
chanRevMotorBL = 14
chanRevMotorBR = 15

SvrFL = Servo90(chanSrvFL)  # передняя левая
SvrFLResolution = (0, 90)   # разрешение

SvrFR = Servo90(chanSvrFR)  # передняя правая
SvrFRResolution = (0, 90)   # разрешение

SvrBL = Servo90(chanSrvBL)  # задняя левая
SvrBLResolution = (0, 90)   # разрешение

SvrBR = Servo90(chanSrvBR)  # задняя правая
SvrBRResolution = (0, 90)   # разрешение

MotorFL = ReverseMotor(chanRevMotorFL)  # моторы, индексы аналогичные
MotorFR = ReverseMotor(chanRevMotorFR)
MotorBL = ReverseMotor(chanRevMotorBL)
MotorBR = ReverseMotor(chanRevMotorBR)

RPCServerPort = 8000    # порт RPC сервера
