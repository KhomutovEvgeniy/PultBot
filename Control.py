""" Модуль описывающий управление роботом """
import Robot
import threading
import time

SEND_DELAY = 0.05  # время задержки отправки новых данных
TURN_STICK = 'rx'  # имя поворотного стика(передняя часть робота)
ROTATE_STICK = 'x' # имя стика танкового разворота
MOVE_STICK = 'ry'  # имя стика движения робота
SPEED_CHANGE_STEP = 10  # размер шага изменения максимальной, при прибавлении или уменьшении с кнопки
ADD_SPEED_BUTTON = 'tr'  # имя кнопки прибавления скорости
SUB_SPEED_BUTTON = 'tl'  # имя кнопки уменьшениия шага
SET_AUTO_BUTTON = 'a'    # имя кнопки установки автономки


class Control(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.robot = Robot.Robot()
        self.joystick = None
        self.EXIT = False
        self.AUTO = False

    def setJoystick(self, joystick):  # устанавливаем джойстик, которым будем управлять
        self.joystick = joystick
        self.connectHandlers()

    def run(self):
        while not self.EXIT:
            try:
                if (self.robot.client is not None) and (self.joystick is not None):  # если клиент создан
                    if not self.AUTO:   # если не автономка
                        if int(self.joystick.Axis.get(ROTATE_STICK)*100.0) == 0:  # если нет танкового разворота
                            self.robot.turn(self.joystick.Axis.get(TURN_STICK))  # поворот
                            self.robot.move(self.joystick.Axis.get(MOVE_STICK))  # движение
                        else:
                            self.robot.rotate(self.joystick.Axis.get(ROTATE_STICK))
                            print(self.joystick.Axis.get(ROTATE_STICK)*self.robot.MotorSpeed)
            except:
                print(111)
            time.sleep(SEND_DELAY)

    def connectHandlers(self):
        def addSpeed():
            self.robot.setMotorsSpeed(self.robot.MotorSpeed + SPEED_CHANGE_STEP)

        def subSpeed():
            self.robot.setMotorsSpeed(self.robot.MotorSpeed - SPEED_CHANGE_STEP)

        def setAuto():
            try:
                self.AUTO = not self.AUTO
                self.robot.client.setAutonomy(self.AUTO)  # инвертируем состоянии автономки
            except:
                self.AUTO = not self.AUTO
                print("Коллизия автономки, попробуйте еще раз")

        self.joystick.connectButton(ADD_SPEED_BUTTON, addSpeed)
        self.joystick.connectButton(SUB_SPEED_BUTTON, subSpeed)
        self.joystick.connectButton(SET_AUTO_BUTTON, setAuto)

    def exit(self):
        self.EXIT = True
