import sender


class SocketRobot:
    def __init__(self):
        self._ip = None
        self._port = None
        self._sender = None
        self._motorSpeed = 0
        self._argDict = {
            "turnForwardArg": float(0.0),
            "moveArg": int(0.0),
            "rotateArg": int(0.0),
            "turnAllArg": float(0.0)
        }

    def connect(self, ip, port):
        self._sender = sender.Sender(ip, port)
        self._sender.packageFormat = "fiif"
        self._sender.connect()

    def _sendPackage(self):
        self._sender.sendPackage(self._sender.pack(
            self._argDict["turnForwardArg"], self._argDict["moveArg"],
            self._argDict["rotateArg"], self._argDict["turnAllArg"]
        ))

    def turnForward(self, scale):  # scale - значение из диапазона (-1, 1)
        # поворачиваем сервами в зависимости от значения со стика
        self._argDict["turnForwardArg"] = float(scale)
        self._sendPackage()

    def move(self, scale):  # scale - значение из диапазона (-1, 1) # движемся вперед со скоростью
        # MotorSpeed*коэффициент scale
        self._argDict["moveArg"] = int(scale * self._motorSpeed)
        self._sendPackage()

    def rotate(self, scale):    # scale - значение из диапазона (-1, 1) # поворачиваемся со скоростью моторов
        # MotorSpeed*коэффициент scale
        self._argDict["rotateArg"] = int(scale * self._motorSpeed)

    def turnAll(self, scale):   # поворачивает всеми сервами на один и тот же угол
        self._argDict["turnAllArg"] = float(scale)

    @property
    def online(self):   # создан ли клиент
        return bool(self._sender)

    @property
    def motorSpeed(self):
        return self._motorSpeed

    @motorSpeed.setter
    def motorSpeed(self, value):    # устанавливаем максимально возможную скорость движения, которая дальше будет
        #  изменяться в некотором диапазоне
        if value >= 100:
            self._motorSpeed = 100
        elif value <= - 100:
            self._motorSpeed = -100
        else:
            self._motorSpeed = value


