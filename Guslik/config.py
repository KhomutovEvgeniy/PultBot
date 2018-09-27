""" Конфигурация робота """
from RPiPWM import *

"""
    F - Front
    B - Backside
    L - Left
    R - Right
"""
IP = '173.1.0.78'  # IP адрес куда отправляем видео
RPCServerPort = 8000  # порт RPC сервера

chanSrvFL = 1  # канал для передней левой сервы
chanSvrFR = 2  # канал для передней правой сервы
chanSrvBL = 3  # канал для задней левой сервы
chanSrvBR = 4  # канал для задней правой сервы
chanSvrCAM = 5  # канал для сервы с камерой
servoResolutionDeg = -90, 90    # разрешение с центром в нуле
servoResolutionMsk = 800, 2400

chanRevMotorLB = 12  # каналы моторов, индексы аналогичны сервам
chanRevMotorRB = 13

SvrFL = Servo270(chanSrvFL)  # передняя левая
SvrFR = Servo270(chanSvrFR)  # передняя правая
SvrBL = Servo270(chanSrvBL)  # задняя левая
SvrBR = Servo270(chanSrvBR)  # задняя правая

MotorLB = ReverseMotor(chanRevMotorLB)  # моторы, индексы аналогичные
MotorRB = ReverseMotor(chanRevMotorRB)


def servoScale(value):  # рескейлим серву, как нам нужно
    degRange = (servoResolutionDeg[1] - servoResolutionDeg[0])
    mskRange = (servoResolutionMsk[1] - servoResolutionMsk[0])
    result = ((value - servoResolutionDeg[0])/degRange) * mskRange + servoResolutionMsk[0]
    if result > servoResolutionMsk[1]:
        return servoResolutionMsk[1]
    elif result < servoResolutionMsk[0]:
        return servoResolutionMsk[0]
    else:
        return int(result)


def rotate(speed):
    """ поворот на месте, speed - скорость поворота """
    pass


def turnForward(scale):
    """ поворот передней части робота """
    SvrFL.SetValue(servoScale(90 * scale))
    SvrFR.SetValue(servoScale(90 * scale))
    return True

def move(speed):
    """ движение вперед/назад """
    MotorLB.SetValue(speed)
    MotorRB.SetValue(-speed)
    return True
