""" Модуль описывающий управление роботом """
import Robot
import threading
import time

SEND_DELAY = 0.05  # время задержки отправки новых данных
TURN_STICK = 'rx'  # имя поворотного стика(передняя часть робота)
MOVE_STICK = 'ry'  # имя стика движения робота
SPEED_CHANGE_STEP = 10  # размер шага изменения максимальной, при прибавлении или уменьшении с кнопки
ADD_SPEED_BUTTON = 'tr'  # имя кнопки прибавления скорости
SUB_SPEED_BUTTON = 'tl'  # имя кнопки уменьшениия шага


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
            if (self.robot.client is not None) and (self.joystick is not None):  # если клиент создан
                self.robot.turn(self.joystick.get(TURN_STICK))  # поворот
                self.robot.move(self.joystick.get(MOVE_STICK))  # движение
            time.sleep(SEND_DELAY)

    def connectHandlers(self):
        def addSpeed():
            self.robot.setMotorsSpeed(self.robot.MotorSpeed + SPEED_CHANGE_STEP)

        def subSpeed():
            self.robot.setMotorsSpeed(self.robot.MotorSpeed - SPEED_CHANGE_STEP)

        self.joystick.connectButton(ADD_SPEED_BUTTON, addSpeed)
        self.joystick.connectButton(SUB_SPEED_BUTTON, subSpeed)

    def exit(self):
        self.EXIT = True
