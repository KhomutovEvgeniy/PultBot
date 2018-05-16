""" Модуль описывающий управление роботом """
import Robot
import threading
import time
from config import *


class Control(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.robot = Robot.Robot()
        self.joystick = None
        self.EXIT = False

    def setJoystick(self, joystick):  # устанавливаем джойстик, которым будем управлять
        self.joystick = joystick
        self.connectHandlers()

    def run(self):
        while not self.EXIT:
            try:
                if (self.robot.client is not None) and (self.joystick is not None):  # если клиент создан
                    if int(self.joystick.Axis.get(ROTATE_STICK)*100.0) == 0:  # если нет разворота на месте в
                        # приближении)
                        self.robot.turn(self.joystick.Axis.get(TURN_STICK))  # поворот
                        self.robot.move(self.joystick.Axis.get(MOVE_STICK))  # движение
                    else:
                        self.robot.rotate(self.joystick.Axis.get(ROTATE_STICK))     # поворот на месте
            except:
                pass
            time.sleep(SEND_DELAY)

    def connectHandlers(self):  # привязка обработчиков кнопок
        def addSpeed():
            self.robot.setMotorsSpeed(self.robot.MotorSpeed + SPEED_CHANGE_STEP)

        def subSpeed():
            self.robot.setMotorsSpeed(self.robot.MotorSpeed - SPEED_CHANGE_STEP)

        def invertAuto():
            try:
                self.robot.invertAutonomy()     # инвертируем состоянии автономки
            except:
                print("Коллизия автономки, попробуйте еще раз")

        self.joystick.connectButton(ADD_SPEED_BUTTON, addSpeed)
        self.joystick.connectButton(SUB_SPEED_BUTTON, subSpeed)
        self.joystick.connectButton(SET_AUTO_BUTTON, invertAuto)

    def exit(self):
        self.EXIT = True
