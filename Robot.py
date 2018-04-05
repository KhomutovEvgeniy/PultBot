import xmlrpc.client


class Robot:
    def __init__(self):
        self.ip = None
        self.port = None
        self.proxy = None
        self.client = None

        """ Разрешения серв """
        self.SFLResolution = None
        self.SFRResolution = None
        self.SBLResolution = None
        self.SBRResolution = None

        """ начальные положения серв """
        self.SFLNullPosition = 0
        self.SFRNullPosition = 0
        self.SBLNullPosition = 0
        self.SBRNullPosition = 0

        self.MotorSpeed = 0

    def connect(self, ip, port):
        self.ip = ip
        self.port = port
        self.proxy = "http://" + ip + ':' + port

        self.client = xmlrpc.client.ServerProxy(self.proxy)
        """ получаем разрешения серв с робота """
        self.SFLResolution = self.client.GetServoResolution("SFL")
        self.SFLResolution = self.SFLResolution[1] - self.SFLResolution[0]

        self.SFRResolution = self.client.GetServoResolution("SFR")
        self.SFRResolution = self.SFRResolution[1] - self.SFRResolution[0]

        self.SBLResolution = self.client.GetServoResolution("SBL")
        self.SBLResolution = self.SBLResolution[1] - self.SBLResolution[0]

        self.SBRResolution = self.client.GetServoResolution("SBR")
        self.SBRResolution = self.SBRResolution[1] - self.SBRResolution[0]

        """ Устанавливаем начальную позицию серв """
        self.SFLNullPosition = self.SFLResolution - int(self.SFLResolution / 2)
        self.SFRNullPosition = self.SFRResolution - int(self.SFRResolution / 2)
        self.SBLNullPosition = self.SBLResolution - int(self.SBLResolution / 2)
        self.SBRNullPosition = self.SBRResolution - int(self.SBRResolution / 2)

    def turn(self,
             scale):  # scale - значение из диапазона (-1, 1)	# поворачиваем сервами в зависимости от значения со стика
        self.client.SetValue("SFL", scale * self.SFLResolution - self.SFLNullPosition)
        self.client.SetValue("SFR", scale * self.SFRResolution - self.SFRNullPosition)

    def move(self, scale):
        self.client.SetValueToAllMotors(scale * self.MotorSpeed)

    def setMotorsSpeed(self, value):
        if value >= 100:
            self.MotorSpeed = 100
        elif value <= - 100:
            self.MotorSpeed = -100
        else:
            self.MotorSpeed = value
