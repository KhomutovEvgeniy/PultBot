import xmlrpc.client


class Robot:    # класс, переносящий ф-ии с робота на пульт
    def __init__(self):
        self._ip = None
        self._port = None
        self._proxy = None
        self._client = None
        self._motorSpeed = 0     # скорость, которую мы подаем на моторы

    def connect(self, ip, port):
        self._ip = ip
        self._port = port
        self._proxy = "http://" + ip + ':' + port
        self._client = xmlrpc.client.ServerProxy(self._proxy)

    def turnForward(self, scale):  # scale - значение из диапазона (-1, 1)
        # 	 поворачиваем сервами в зависимости от значения со стика
        self._client.turnForward(scale)

    def move(self, scale):  # scale - значение из диапазона (-1, 1) # движемся вперед со скоростью
        # MotorSpeed*коэффициент scale
        self._client.move(int(scale * self._motorSpeed))

    def rotate(self, scale):    # scale - значение из диапазона (-1, 1) # поворачиваемся со скоростью моторов
        # MotorSpeed*коэффициент scale
        self._client.rotate(int(scale * self._motorSpeed))

    def turnAll(self, scale):   # поворачивает всеми сервами на один и тот же угол
        self._client.turnAll(scale)

    @property
    def online(self):   # создан ли клиент
        return bool(self._client)

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



