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
            "turnAll": EventBlock("turnAll")
        }
        self._oldPackage = [None, None, None, None]
        self._eventMaster = EventMaster()
        self._eventMaster.append(self._eventDict.get("turnForward"))
        self._eventMaster.append(self._eventDict.get("move"))
        self._eventMaster.append(self._eventDict.get("rotate"))
        self._eventMaster.append(self._eventDict.get("turnAll"))
        self._eventMaster.start()

    def connect(self, ip, port):
        self._receiver = receiver.Receiver(ip, port)
        self._receiver.packageFormat = "fiif"

        def onReceive(data):
            if data[0] != self._oldPackage[0]:
                self._eventDict["turnForward"].push(data[0])

            if data[1] != self._oldPackage[1]:
                self._eventDict["move"].push(data[1])

            if data[2] != self._oldPackage[2]:
                self._eventDict["rotate"].push(data[2])

            if data[3] != self._oldPackage[3]:
                self._eventDict["turnAll"].push(data[3])

        self._receiver.connectToEvent(onReceive, "onReceive")
        self._receiver.connect()

    def connectToEvent(self, foo, toEvent):
        event = self._eventDict.get(toEvent)
        if not event:
            print("Такого события нет")
        event.setfun(foo)
