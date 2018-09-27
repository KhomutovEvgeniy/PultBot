#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from RTCJoystick import Joystick
from Control import Control
from config import *

joystick = Joystick()
joystick.connect("/dev/input/js0")

control = Control()
control.setJoystick(joystick)
control.robot.connect(IP, PORT)

joystick.start()
control.start()



