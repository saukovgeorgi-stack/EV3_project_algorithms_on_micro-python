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

def moving():
    motor_r.run_angle(500, 360, wait=False)
    motor_l.run_angle(500,360, wait=True)
    wait(10)
    motor_l.stop()
    motor_r.stop()

def pid(): #simple PID-controller
    global last_error, state, target, dis_r, dis_l

    error = dis_r - target
    if error > last_error + 30 or error < last_error -30:
        moving()
        print("moving_pid")
        motor_l.run_angle(600, 350, wait=False) #(speed, angle, wait)
        motor_r.run_angle(600, -350, wait=True) #the turning angle depends on your wheels, so choose it to suit yourself
        print("right turning")
        moving()
        print("moving_pid")
        rollback()
    else:
        motor_r.run(-error*5)
        motor_l.run(error*5)
        print("pid")
    last_error = error

def rollback(): #function to reset all temporary variables 
    global target, error, last_error

    target = 0
    error = 0
    last_error = 0

last_error = 0
target = 0
error = 0

state = 0

while True:
    dis_f, dis_r, dis_l = get_distances() #this function is not optimised, but now it's OK

    if dis_f < 150: #distance is in mm so it's 15 cm
        motor_l.run_angle(400, -350, wait=False) #(speed, angle, wait)
        motor_r.run_angle(400, 350, wait=True) #the turning angle depends on your wheels, so choose it to suit yourself
        print("left turning")
        wait(10)
        motor_l.stop()
        motor_r.stop()
        rollback()
    elif target == 0:
        target = dis_r
    elif dis_r < target-2 or dis_r > target+2:
        pid()
    else:
        motor_r.run(500)
        motor_l.run(500)
        print("moving")

    wait(10) #wait for high-quality cycle processing
