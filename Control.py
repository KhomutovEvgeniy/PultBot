""" Модуль описывающий управление роботом """
import Robot
import threading
import time
from config import *
import SocketRobot


class Control(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self, daemon=True)
        self.robot = SocketRobot.SocketRobot()
        self._joystick = None
        self._EXIT = False

    def setJoystick(self, joystick):  # устанавливаем джойстик, которым будем управлять
        self._joystick = joystick
        self.connectHandlers()

    def run(self):
        while not self._EXIT:
            try:
                if self.robot.online and (self._joystick is not None):  # если клиент и джойстик созданы
                    if int(self._joystick.Axis.get(ROTATE_STICK)*100.0) == 0:  # если нет разворота на месте в
                        # приближении(некоторые стики повреждены))
                        self.robot.turnForward(self._joystick.Axis.get(TURN_STICK))  # поворот
                        self.robot.move(self._joystick.Axis.get(MOVE_STICK))  # движение
                    else:
                        self.robot.rotate(self._joystick.Axis.get(ROTATE_STICK))     # поворот на месте
                        pass
            except:
                print("Ошибка управления")
            time.sleep(SEND_DELAY)

    def connectHandlers(self):  # привязка обработчиков кнопок
        def addSpeed(w):
            if w:
                self.robot.motorSpeed += SPEED_CHANGE_STEP     # прибавляем скорость

        def subSpeed(w):
            if w:
                self.robot.motorSpeed -= SPEED_CHANGE_STEP     # уменьшаем скорость

        self._joystick.connectButton(ADD_SPEED_BUTTON, addSpeed)
        self._joystick.connectButton(SUB_SPEED_BUTTON, subSpeed)

    def exit(self):
        self._EXIT = True
