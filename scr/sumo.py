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

        self.search_dir = 1
        self.state = "SEARCHING"

    def read_front(self):
        dist = self.us_f.distance()
        return dist
    
    def searching(self):
        self.motor_l.dc(80*self.search_dir)
        self.motor_r.dc(80*-self.search_dir)

        dist_f = self.read_front()

        if dist_f <= 700:
            self.motor_l.brake()
            self.motor_r.brake()

            self.state = "PERSECUTION"

    def persecution(self):
        dist_f = self.read_front()

        if dist_f < 250:
            self.state = "ATTACK"

        elif dist_f > 700:
            dist_l = self.us_l.distance()
            dist_r = self.us_r.distance()

            if dist_l < dist_r:
                self.search_dir = -1
            else:
                self.search_dir = 1
            self.state = "SEARCHING"
        
        else:
            self.motor_l.run(900)
            self.motor_r.run(900)

    def attack(self):
        self.motor_l.dc(80)
        self.motor_r.dc(80)

        dist_f = self.us_f.distance()

        if dist_f > 700:
            self.state = "SEARCHING"

    def run(self):
        self.ev3.speaker.beep()

        while True:
            if self.state == "SEARCHING":
                self.searching()
            elif self.state == "PERSECUTION":
                self.persecution()
            elif self.state == "ATTACK":
                self.attack()

            wait(10)

try:
    if __name__ == "__main__":
        Sumo()
except KeyboardInterrupt

