import receiver
from RTCEventMaster import EventMaster, EventBlock


class Control:
    def __init__(self):
        self._ip = None
        self._port = None
        self._receiver = None
        self._eventDict = {
            "turnForward": EventBlock("turnForward"),
            "move": EventBlock("move"),
            "rotate": EventBlock("rotate"),
            "turnAll": EventBlock("turnAll"),
            "setAuto": EventBlock("setAuto"),
            "setCamera": EventBlock("setCamera")
        }
        self._oldPackage = [None, None, None, None, None, None]
        self._eventMaster = EventMaster()
        self._eventMaster.append(self._eventDict.get("turnForward"))
        self._eventMaster.append(self._eventDict.get("move"))
        self._eventMaster.append(self._eventDict.get("rotate"))
        self._eventMaster.append(self._eventDict.get("turnAll"))
        self._eventMaster.append(self._eventDict.get("setAuto"))
        self._eventMaster.append(self._eventDict.get("setCamera"))
        self._eventMaster.start()

    def connect(self, ip, port):
        self._receiver = receiver.Receiver(ip, port)
        self._receiver.packageFormat = "fiif?f"

        def onReceive(data):
            if data[0] != self._oldPackage[0]:
                self._eventDict["turnForward"].push(data[0])

            if data[1] != self._oldPackage[1]:
                self._eventDict["move"].push(data[1])

            if data[2] != self._oldPackage[2]:
                self._eventDict["rotate"].push(data[2])

            if data[3] != self._oldPackage[3]:
                self._eventDict["turnAll"].push(data[3])

            if data[4] != self._oldPackage[4]:
                self._eventDict["setAuto"].push(data[4])

            if data[5] != self._oldPackage[5]:
                self._eventDict["setCamera"].push(data[5])

            self._oldPackage = data[:]

        self._receiver.connectToEvent(onReceive, "onReceive")
        self._receiver.connect()

    def connectToEvent(self, foo, toEvent):
        event = self._eventDict.get(toEvent)
        if not event:
            print("Такого события нет")
        event.setfun(foo)
