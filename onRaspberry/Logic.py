""" Логика работы робота """
import onRaspberry.RPiPWM
from onRaspberry.config import *


def SetValue(dev, value):   # установка значения на
    if dev == "SFL":    # поворот передней левой сервой
        SvrFL.SetValue(value)
    elif dev == "SFR":  # поворот передней правой сервой
        SvrFR.SetValue(value)
    elif dev == "SBL":  # поворот задней левой сервой
        SvrBL.SetValue(value)
    elif dev == "SBR":  # поворот задней правой сервой
        SvrBR.SetValue(value)

    elif dev == "MFL":  # изменение скорости переднего левого мотора
        MotorFL.SetValue(value)
    elif dev == "MFR":  # изменение скорости переднего правого мотора
        MotorFR.SetValue(value)
    elif dev == "MBL":  # изменения скорости заднего левого мотора
        MotorBL.SetValue(value)
    elif dev == "MBR":  # изменение скорости заднего правого мотора
        MotorBR.SetValue(value)
    else:   # если ни одно из этих значений
        return False
    return True     # если все получилось


def GetServoResolution(srv):
    res = None
    if srv == "SFL":    # поворот передней левой сервой
        res = SvrFLResolution
    elif srv == "SFR":  # поворот передней правой сервой
        res = SvrFRResolution
    elif srv == "SBL":  # поворот задней левой сервой
        res = SvrBLResolution
    elif srv == "SBR":  # поворот задней правой сервой
        res = SvrBRResolution
    return res
