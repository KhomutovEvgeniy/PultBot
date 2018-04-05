""" Логика работы робота """
from config import *
import camera


def setSpeedToAllMotors(value):
    if not camera.AUTO:
        MotorFL.SetValue(value)
        MotorFR.SetValue(value)
        MotorBL.SetValue(value)
        MotorBR.SetValue(value)
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
        SetValueToAllMotors(speed)


def setAutonomy(b):
    SvrCAM.setValue(0)
    camera.setAUTO(b)
    return True


def getAUTO():
    return camera.AUTO


