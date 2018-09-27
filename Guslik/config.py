""" Конфигурация робота """
from RPiPWM import *

"""
    F - Front
    B - Backside
    L - Left
    R - Right
"""
IP = '173.1.0.92'  # IP адрес куда отправляем видео
RPCServerPort = 8000  # порт RPC сервера

chanSrvFL = 1  # канал для передней левой сервы
chanSvrFR = 2  # канал для передней правой сервы
chanSrvBL = 3  # канал для задней левой сервы
chanSrvBR = 4  # канал для задней правой сервы
chanSvrCAM = 5  # канал для сервы с камерой

chanRevMotorLB = 12  # каналы моторов, индексы аналогичны сервам
chanRevMotorRB = 13

SvrFL = Servo270(chanSrvFL)  # передняя левая
SvrFR = Servo270(chanSvrFR)  # передняя правая
SvrBL = Servo270(chanSrvBL)  # задняя левая
SvrBR = Servo270(chanSrvBR)  # задняя правая

MotorLB = ReverseMotor(chanRevMotorLB)  # моторы, индексы аналогичные
MotorRB = ReverseMotor(chanRevMotorRB)


def rotate(speed):
    """ поворот на месте, speed - скорость поворота """
    pass


def turnForward(scale):
    """ поворот передней части робота """
    pass


def move(speed):
    """ движение вперед/назад """
    pass

