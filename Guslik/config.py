""" Конфигурация робота """
from RPiPWM import *

"""
    F - Front
    B - Backside
    L - Left
    R - Right
"""
IP = '173.1.0.78'  # IP адрес куда отправляем видео
RPCServerPort = 9000  # порт RPC сервера
INTENSIVITY = 110
RTP_PORT = 5000
PORT = 8000

chanSrvFL = 8  # канал для передней левой сервы
chanSvrFR = 6  # канал для передней правой сервы
chanSrvBL = 11  # канал для задней левой сервы
chanSrvBR = 9  # канал для задней правой сервы
chanSvrCAM = 7  # канал для сервы с камерой

chanRevMotorLB = 14  # каналы моторов, индексы аналогичны сервам
chanRevMotorRB = 15

servoResolutionDeg = -90, 90    # разрешение с центром в нуле
servoResolutionMcs = 800, 2400
cameraResolutionDeg = 0, 35     # разрешение камеры в градусах
rotateAngle = 57.76     # угол в градусах, на который надо повернуть сервы, чтобы робот крутился на месте
# для квадратных роботов это 45 градусов

SENSIVITY = 108     # чувствительность автономки

SvrFL = Servo270(chanSrvFL)  # передняя левая
SvrFR = Servo270(chanSvrFR)  # передняя правая
SvrBL = Servo270(chanSrvBL)  # задняя левая
SvrBR = Servo270(chanSrvBR)  # задняя правая
SvrCAM = Servo90(chanSvrCAM)

MotorLB = ReverseMotor(chanRevMotorLB)  # моторы, индексы аналогичные
MotorRB = ReverseMotor(chanRevMotorRB)

global AUTO
AUTO = False    # флаг автономки


def servoScale(value):  # рескейлим серву, как нам нужно
    degRange = (servoResolutionDeg[1] - servoResolutionDeg[0])
    mskRange = (servoResolutionMcs[1] - servoResolutionMcs[0])
    result = ((value - servoResolutionDeg[0])/degRange) * mskRange + servoResolutionMcs[0]
    if result > servoResolutionMcs[1]:
        return servoResolutionMcs[1]
    elif result < servoResolutionMcs[0]:
        return servoResolutionMcs[0]
    else:
        return int(result)


def rotate(speed):
    """ поворот на месте, speed - скорость поворота """
    global AUTO
    if not AUTO:
        if abs(speed) < 10:
            SvrFL.SetMcs(servoScale(0))
            SvrFR.SetMcs(servoScale(0))
            SvrBL.SetMcs(servoScale(0))
            SvrBR.SetMcs(servoScale(0))
            MotorRB.SetValue(0)
            MotorLB.SetValue(0)
        else:
            SvrFL.SetMcs(servoScale(rotateAngle))
            SvrFR.SetMcs(servoScale(-rotateAngle))
            SvrBL.SetMcs(servoScale(-rotateAngle))
            SvrBR.SetMcs(servoScale(rotateAngle))
            MotorRB.SetValue(speed)
            MotorLB.SetValue(speed)
    return True


def turnAll(scale):
    """ поворот всех серв на один угол"""
    global AUTO
    if not AUTO:
        result = servoScale(90 * scale)
        SvrFL.SetMcs(result)
        SvrFR.SetMcs(result)
        SvrBL.SetMcs(result)
        SvrBR.SetMcs(result)
    return True


def turnForwardit(scale):
    """ поворот передней части робота """
    SvrBR.SetMcs(servoScale(-rotateAngle * scale))
    SvrBL.SetMcs(servoScale(-rotateAngle * scale))
    SvrFL.SetMcs(servoScale(rotateAngle * scale))
    SvrFR.SetMcs(servoScale(rotateAngle * scale))


def turnForward(scale):
    """ поворот передней части робота """
    global AUTO
    if not AUTO:
        SvrBR.SetMcs(servoScale(0))
        SvrBL.SetMcs(servoScale(0))
        SvrFL.SetMcs(servoScale(rotateAngle * scale))
        SvrFR.SetMcs(servoScale(rotateAngle * scale))
    return True


def moveit(speed):
    MotorLB.SetValue(-speed)
    MotorRB.SetValue(speed)


def move(speed):
    """ движение вперед/назад """
    global AUTO
    if not AUTO:
        moveit(speed)
    return True


def setCamera(scale):
    """ установить камеру в нужное положение """
    resolution = cameraResolutionDeg[1] - cameraResolutionDeg[0]
    if scale * resolution > cameraResolutionDeg[1]:
        result = cameraResolutionDeg[1]
    elif scale * resolution < cameraResolutionDeg[0]:
        result = cameraResolutionDeg[0]
    else:
        result = scale * resolution
    SvrCAM.SetValue(result)


def setAuto(b):
    """ Установка автономности """
    global AUTO
    AUTO = b
