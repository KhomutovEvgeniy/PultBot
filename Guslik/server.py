#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Сервер, установленный на малине """
from xmlrpc.server import SimpleXMLRPCServer
import subprocess
from config import *
import camera
import Control
import time

"""
cmd = 'hostname -I | cut -d\' \' -f1'
selfIP = subprocess.check_output(cmd, shell=True)     # получаем IP
selfIP.rstrip().decode("utf-8")     # удаляем \n, переводим в текст

server = SimpleXMLRPCServer((selfIP, RPCServerPort), logRequests=False)

server.register_function(turnForward)
server.register_function(turnAll)
server.register_function(rotate)
server.register_function(move)
camera.start()

server.serve_forever()
"""

control = Control.Control()
control.connectToEvent(turnForward, "turnForward")
control.connectToEvent(turnAll, "turnAll")
control.connectToEvent(rotate, "rotate")
control.connectToEvent(move, "move")
control.connect('', PORT)
camera.start()

while True:
    time.sleep(1)


