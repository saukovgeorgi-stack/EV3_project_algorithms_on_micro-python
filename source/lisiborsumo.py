#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, UltrasonicSensor
from pybricks.parameters import Port
from pybricks.tools import wait

#constans
ATTACK_SPEED = 1100
SEARCH_SPEED = 900

ev3 = EV3Brick()

us_f = UltrasonicSensor(Port. S2)
us_l = UltrasonicSensor(Port. S4)
us_r = UltrasonicSensor(Port. S3)

motor_r = Motor(Port. B)
motor_l = Motor(Port. C)
axis = Motor(Port. A)

def moving(speed):
    motor_l.run(speed)
    motor_r.run(speed)

first_c = False

axis.run_angle(900, -220, wait=True)

while True:
    ds_f = us_f.distance()
    ds_r = us_r.distance()
    ds_l = us_l.distance()

    if first_c == False:
        if ds_f <= 700:
            motor_r.hold()
            motor_l.hold()
        elif ds_r < 700:
            motor_l.run(900)
            motor_r.run(-900)
        else:
            motor_l.run(-900)
            motor_r.run(900)
        first_c = True

    elif ds_f <= 700:
        moving(1300)
    else:
        motor_r.run(-900)
        motor_l.run(900)
    
