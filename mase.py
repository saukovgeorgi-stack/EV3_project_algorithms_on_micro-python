#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, UltrasonicSensor
from pybricks.parameters import Port, Stop, Direction
from pybricks.tools import wait

ev3 = EV3Brick()

motor_r = Motor(Port.B)
motor_l = Motor(Port.C) #motors

us_f = UltrasonicSensor(Port.S3)
us_r = UltrasonicSensor(Port.S4) #sensors 
us_l = UltrasonicSensor(Port.S2)

def get_distances():
    dis_f = us_f.distance()
    dis_r = us_r.distance()
    dis_l = us_l.distance()
    return dis_f, dis_r, dis_l
while True:
    dis_f, dis_r, dis_l = get_distances() #this function is not optimised, but now it's OK

    if dis_f < 150: #distance is in mm so it's 15 cm
        motor_l.run_angle(600, -250, wait=False) #(speed, angle, wait)
        motor_r.run_angle(600, 250, wait=True) #the turning angle depends on your wheels, so choose it to suit yourself
        print("left turning")
        break
    else:
        motor_r.run(500)
        motor_l.run(500)
        print("moving")

    wait(10) #wait for high-quality cycle processing
