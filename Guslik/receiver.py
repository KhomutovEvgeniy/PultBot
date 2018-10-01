import socket
import time
import threading
import struct
import RTCEventMaster


class Receiver(threading.Thread):
    def __init__(self, ip, port):
        threading.Thread.__init__(self, daemon=True)
        self._connected = False
        self._ip = ip
        self._port = port
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._conn = None
        self._exit = False
        self._eventDict = {"onReceive": RTCEventMaster.EventBlock("onReceive")}
        self._eventMaster = RTCEventMaster.EventMaster()
        self._eventMaster.append(self._eventDict.get("onReceive"))
        self._eventMaster.start()
        self._packageFormat = 'ffff'

    def connect(self):
        if not self._connected:
            try:
                self._sock.bind((self._ip, self._port))
                self._sock.listen(1)
                self._conn, _ = self._sock.accept()
                self._connected = True
                self.start()
            except:
                print("can't connect to", self._ip)

    def disconnect(self):
        self._sock.close()
        self._connected = False

    def connectToEvent(self, foo, toEvent):
        event = self._eventDict.get(toEvent)
        if event:
            event.setfun(foo)
        else:
            print("Такого события нет")

    def run(self):
        while not self._exit:
            try:
                data = self._conn.recv(struct.calcsize(self._packageFormat))
                self._eventDict.get("onReceive").push(struct.unpack(self._packageFormat, data))
            except:
                print("Проблемы с приемом")
            time.sleep(0.01)

    @property
    def packageFormat(self):
        return self._packageFormat

    @packageFormat.setter
    def packageFormat(self, format):
        self._packageFormat = format