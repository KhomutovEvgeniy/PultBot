import xmlrpc.client


class Robot:
    def __init__(self):
        self.ip = None
        self.port = None
        self.proxy = None
        self.client = None
        self.Autonomy = False   # метка автономности

        self.MotorSpeed = 0

    def connect(self, ip, port):
        self.ip = ip
        self.port = port
        self.proxy = "http://" + ip + ':' + port

        self.client = xmlrpc.client.ServerProxy(self.proxy)

    def turn(self,
             scale):  # scale - значение из диапазона (-1, 1)	# поворачиваем сервами в зависимости от значения со стика
        self.client.turnForward(scale)

    def move(self, scale):
        self.client.setSpeedToAllMotors(scale * self.MotorSpeed)

    def rotate(self, scale):
        self.client.rotate(scale * self.MotorSpeed)

    def setAutonomy(self, b):
        self.client.setAutonomy(b)

    def setMotorsSpeed(self, value):
        if value >= 100:
            self.MotorSpeed = 100
        elif value <= - 100:
            self.MotorSpeed = -100
        else:
            self.MotorSpeed = value
