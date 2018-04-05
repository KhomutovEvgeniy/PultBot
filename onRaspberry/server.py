#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Сервер, установленный на малине """
from xmlrpc.server import SimpleXMLRPCServer
import subprocess
from config import *
from Logic import *
import camera

cmd = 'hostname -I | cut -d\' \' -f1'
selfIP = subprocess.check_output(cmd, shell=True)     # получаем IP
selfIP.rstrip().decode("utf-8")     # удаляем \n, переводим в текст
camera.rpiCamStreamer.start()  # запускаем трансляцию
camera.frameHandlerThread.start()  # запускаем обработку


server = SimpleXMLRPCServer((selfIP, RPCServerPort))

server.register_function(turnForward)
server.register_function(rotate)
server.register_function(setSpeedToAllMotors)
server.register_function(setAutonomy)
server.register_function(getAUTO)

server.serve_forever()





