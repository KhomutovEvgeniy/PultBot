import xmlrpc.client


class Robot:    # класс, переносящий ф-ии с робота на пульт
    def __init__(self):
        self.ip = None
        self.port = None
        self.proxy = None
        self.client = None
        self.Autonomy = False   # метка автономности
        self.MotorSpeed = 0     # скорость, которую мы подаем на моторы

    def connect(self, ip, port):
        self.ip = ip
        self.port = port
        self.proxy = "http://" + ip + ':' + port
        self.client = xmlrpc.client.ServerProxy(self.proxy)

    def turn(self,
             scale):  # scale - значение из диапазона (-1, 1)	# поворачиваем сервами в зависимости от значения со стика
        self.client.turnForward(scale)

    def move(self, scale):  # scale - значение из диапазона (-1, 1) # движемся вперед со скоростью
        # MotorSpeed*коэффициент scale
        self.client.setSpeedToAllMotors(int(scale * self.MotorSpeed))

    def rotate(self, scale):    # scale - значение из диапазона (-1, 1) # поворачиваемся со скоростью моторов
        # MotorSpeed*коэффициент scale
        self.client.rotate(int(scale * self.MotorSpeed))

    def setMotorsSpeed(self, value):    # устанавливаем максимально возможную скорость движения, которая дальше будет
        #  изменяться в некотором диапазоне
        if value >= 100:
            self.MotorSpeed = 100
        elif value <= - 100:
            self.MotorSpeed = -100
        else:
            self.MotorSpeed = value

    def invertAutonomy(self):   # инвертирует состояние автономки
        self.client.invertAutonomy()

    def online(self, a, b):
        self.client.online(a, b)


