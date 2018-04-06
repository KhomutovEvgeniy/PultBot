""" Логика работы робота """
from config import *
import camera


def setSpeedToAllMotors(value):
    if not camera.AUTO:
        MotorLB.SetValue(value)
        MotorRB.SetValue(value)
    return True


def turnForward(scale):  # поворот передней части робота
    if not camera.AUTO:
        tempFL = int((SvrFLResolution[1] - SvrFLResolution[0]) / 2)
        tempFR = int((SvrFRResolution[1] - SvrFRResolution[0]) / 2)
        SvrFL.SetValue(int(scale * tempFL) + tempFL)
        SvrFR.SetValue(int(scale * tempFR) + tempFR)
    return True


def rotate(speed):
    if not camera.AUTO:
        SvrFL.SetValue(0)
        SvrFR.SetValue(90)
        SvrBL.SetValue(90)
        SvrBR.SetValue(0)
        SetSpeedToAllMotors(speed)
    return True


def setAutonomy(b):     # ее запихиваем в сервер
    if b:
        SvrCAM.SetValue(0)
    else:
        SvrCAM.SetValue(int((SvrCAMResolution[1] - SvrCAMResolution[0]) / 2))
    camera.frameHandlerThread.setAutonomy(b)



