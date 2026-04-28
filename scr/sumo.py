#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import UltrasonicSensor, ColorSensor,  Motor
from pybricks.parameters import Port, Stop
from pybricks.tools import wait, StopWatch

class Sumo:
    def __init__(self):
        self.ev3 = EV3Brick()
        self.us_f = UltrasonicSensor(Port.S2)
        self.us_l = UltrasonicSensor(Port.S4) #adjust these values depending on the robot's ports
        self.us_r = UltrasonicSensor(Port.S3)

        self.motor_l = Motor(Port.C)
        self.motor_r = Motor(Port.B)

