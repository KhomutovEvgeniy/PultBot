import gi
import GstDrawingArea
import RTCjoystick
import Control

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class InterfaceBot:
    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("interface.glade")
        self.window = self.builder.get_object("window1")
        self.window.connect("delete-event", self.delete_event)
        """ Вытаскиваем данные из .glade """
        self.joystickSwitch = self.builder.get_object("JoystickSwitch")
        self.cameraSwitch = self.builder.get_object("CameraSwitch")

        self.joystickEntry = self.builder.get_object("JoystickEntry")
        self.cameraEntry = self.builder.get_object("CameraEntry")
        self.robotIpEntry = self.builder.get_object("RobotIpEntry")  # ДОБАВИТЬ
        self.robotPortEntry = self.builder.get_object("RobotPortEntry")	# ДОБАВИТЬ

        self.logView = self.builder.get_object("LogView")
        self.logBuffer = self.logView.get_buffer()

        self.clearLogButton = self.builder.get_object("ClearLogButton")
        self.startButton = self.builder.get_object("StartButton")
        self.pauseButton = self.builder.get_object("PauseButton")
        self.stopButton = self.builder.get_object("StopButton")
        self.toAppSinkButton = self.builder.get_object("ToAppSinkButton")
        self.toAutoVideoSinkButton = self.builder.get_object("ToAutoVideoSinkButton")
        self.connectToRobotButton = self.builder.get_object("ConnectToRobotButton")  # ДОБАВИТЬ

        self.clearLogButton.connect("clicked", self.clearLogButton_Click)
        self.startButton.connect("clicked", self.startButton_Click)
        self.stopButton.connect("clicked", self.stopButton_Click)
        self.pauseButton.connect("clicked", self.pauseButton_Click)
        self.toAppSinkButton.connect("clicked", self.toAppSinkButton_Click)
        self.toAutoVideoSinkButton.connect("clicked", self.toAutoVideoSinkButton_Click)
        self.connectToRobotButton.connect("clicked", self.connectToRobotButton_Click)

        self.joystickSwitch.connect("state-set", self.joystickSwitch_Click)
        self.cameraSwitch.connect("state-set", self.cameraSwitch_Click)

        self.videoBox = self.builder.get_object("VideoBox")  # бокс, куда пакуем виджет-видео

        self.gstDrawingArea = GstDrawingArea.GstDrawingArea()  # виджет-видео
        self.videoBox.pack_start(self.gstDrawingArea, True, True, 0)
        self.control = Control.Control()  # заглушка управления роботом

        self.joystick = None
        try:
            if self.joystickSwitch.get_active():
                self.joystick = RTCjoystick.Joystick()  # Джойстик
                self.joystick.connect(self.joystickEntry.get_text())
                self.control.setJoystick(self.joystick)
        except:
            self.printLog("Такого джойстика нет")

        self.window.show_all()

    def delete_event(self, widget, event, data=None):
        if self.gstDrawingArea.source is not None:
            self.gstDrawingArea.source.stop()
            self.gstDrawingArea.source = None
        if self.joystick is not None:
            self.joystick.exit()
        self.control.exit()
        Gtk.main_quit()

    def printLog(self, string):  # печать логов в конец LogView
        endIter = self.logBuffer.get_end_iter()
        self.logBuffer.insert(endIter, string + "\n")

    def clearLogButton_Click(self, w):  # обработчик нажатия кнопки clearLogButton
        self.logBuffer.set_text("")

    def startButton_Click(self, w):  # обработчик нажатия кнопки startButton
        if self.gstDrawingArea.source is None:
            try:
                if self.cameraSwitch.get_active():
                    ip = self.cameraEntry.get_text()
                    self.gstDrawingArea.setSource(IP=ip)
                    self.gstDrawingArea.source.start()
                    self.printLog("Ресурс камеры создан")
                else:
                    self.printLog("Камера отключена")
            except:
                self.printLog("Не получается воспроизвести видеоресурс")
        else:
            try:
                self.gstDrawingArea.source.start()
            except:
                self.printLog("Видео уже запущено")

    def stopButton_Click(self, w):  # обработчик нажатия кнопки stopButton
        if self.gstDrawingArea.source is not None:
            try:
                self.gstDrawingArea.source.stop()
                self.gstDrawingArea.source = None
            except:
                self.printLog("Не получается остановить видеоресурс")
        else:
            self.printLog("Ресурс камеры не создан")

    def pauseButton_Click(self, w):  # обработчик нажатия кнопки pauseButton
        if self.gstDrawingArea.source is not None:
            try:
                self.gstDrawingArea.source.paused()
            except:
                self.printLog("Не получается поставить на паузу видеоресурс")
        else:
            self.printLog("Ресурс камеры не создан")

    def toAppSinkButton_Click(self, w):  # обработчик нажатия кнопки toAppSinkButton
        if self.gstDrawingArea.source is not None:
            self.gstDrawingArea.source.toAppSink()
        else:
            self.printLog("Ресурс камеры не создан")

    def toAutoVideoSinkButton_Click(self, w):  # обработчик нажатия кнопки toAutoVideoSinkButton
        if self.gstDrawingArea.source is not None:
            self.gstDrawingArea.source.toAutoVideoSink()
        else:
            self.printLog("Ресурс камеры не создан")

    def joystickSwitch_Click(self, w, state):
        if state:
            if self.joystick is None:  # если до этого джойстик не был создан
                try:
                    self.joystick = RTCjoystick.Joystick()
                    self.joystick.connect(self.joystickEntry.get_text())
                    self.control.setJoystick(joystick)
                except:
                    self.printLog("Такого Джойстика нет")
            else:
                pass
        else:
            if self.joystick is not None:
                self.joystick.exit()
                self.joystick = None
                self.printLog("Джойстик удален")
            else:
                pass

    def cameraSwitch_Click(self, w, state):
        if state:
            pass
        else:
            try:
                self.gstDrawingArea.source.stop()
                self.gstDrawingArea.source = None
                self.printLog("Камера удалена")
            except:
                self.printLog("Не удалось удалить камеру")

    def connectToRobotButton_Click(self, w):
        self.control.robot.connect(self.robotIpEntry.get_text(), self.robotPortEntry.get_text())


a = InterfaceBot()
Gtk.main()
