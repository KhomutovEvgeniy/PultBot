#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Сервер, установленный на малине """
from xmlrpc.server import SimpleXMLRPCServer
import subprocess
from onRaspberry.config import *
from onRaspberry.Logic import *

cmd = 'hostname -I | cut -d\' \' -f1'
selfIP = subprocess.check_output(cmd, shell=True)     # получаем IP
selfIP.rstrip().decode("utf-8")     # удаляем \n, переводим в текст

server = SimpleXMLRPCServer((selfIP, RPCServerPort))

server.register_function(SetValue)
server.register_function(GetServoResolution)

server.serve_forever()





