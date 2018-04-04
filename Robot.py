import xmlrpc.client


class Robot:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.proxy = "http://" + ip + ':' + port
        self.client = None

        self.SFLResolution = None
        self.SFRResolution = None
        self.SBLResolution = None
        self.SBRResolution = None

        self.SFLPosition = 0
        self.SFRPosition = 0
        self.SBLPosition = 0
        self.SBRPosition = 0

        self.MotorSpeed = 0

    def connect(self):
        self.client = xmlrpc.client.ServerProxy(self.proxy)
        """ получаем разрешения серв с робота """
        self.SFLResolution = self.client.GetServoResolution("SFL")
        self.SFRResolution = self.client.GetServoResolution("SFR")
        self.SBLResolution = self.client.GetServoResolution("SBL")
        self.SBRResolution = self.client.GetServoResolution("SBR")

        """ Устанавливаем начальную позицию серв """
        self.SFLPosition = self.SFLResolution - int(self.SFLResolution / 2)
        self.SFRPosition = self.SFRResolution - int(self.SFRResolution / 2)
        self.SBLPosition = self.SBLResolution - int(self.SBLResolution / 2)
        self.SBRPosition = self.SBRResolution - int(self.SBRResolution / 2)

    def rotateRobot(self, scale):   # scale - значение из диапазона (-1, 1)
        pass