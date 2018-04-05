""" Логика работы робота """
from onRaspberry.config import *


def SetValue(dev, value):  # установка значения на
    if dev == "SFL":  # поворот передней левой сервой
        SvrFL.SetValue(value)
    elif dev == "SFR":  # поворот передней правой сервой
        SvrFR.SetValue(value)
    elif dev == "SBL":  # поворот задней левой сервой
        SvrBL.SetValue(value)
    elif dev == "SBR":  # поворот задней правой сервой
        SvrBR.SetValue(value)
    elif dev == "SCM":  # поворот сервы с камерой
        SvrCAM.SetValue(value)

    elif dev == "MFL":  # изменение скорости переднего левого мотора
        MotorFL.SetValue(value)
    elif dev == "MFR":  # изменение скорости переднего правого мотора
        MotorFR.SetValue(value)
    elif dev == "MBL":  # изменения скорости заднего левого мотора
        MotorBL.SetValue(value)
    elif dev == "MBR":  # изменение скорости заднего правого мотора
        MotorBR.SetValue(value)
    else:  # если ни одно из этих значений
        return False
    return True  # если все получилось


def SetValueToAllMotors(value):
    MotorFL.SetValue(value)
    MotorFR.SetValue(value)
    MotorBL.SetValue(value)
    MotorBR.SetValue(value)


def GetServoResolution(srv):  # возвращает разрешение сервы
    res = None
    if srv == "SFL":  # левая серва
        res = SvrFLResolution
    elif srv == "SFR":  # правая серва
        res = SvrFRResolution
    elif srv == "SBL":  # задняя левая серва
        res = SvrBLResolution
    elif srv == "SBR":
        res = SvrBRResolution
    return res
