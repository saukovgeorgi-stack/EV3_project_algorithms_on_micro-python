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

    if dis_f == 2550: dis_f = 9999
    if dis_r == 2550: dis_r = 9999
    if dis_l == 2550: dis_l = 9999
    return dis_f, dis_r, dis_l

def moving(multiplier):
    motor_r.stop()
    motor_l.stop()
    motor_r.run_angle(700, 360*multiplier, wait=False)
    motor_l.run_angle(700, 360*multiplier, wait=True)
    motor_l.stop()
    motor_r.stop()

def pid(): #simple PID-controller
    global last_error, error, attempt_count, state, target, dis_r, dis_l

    error = dis_r - target
    if error > last_error+15 or error > 150:
        if attempt_count > 2:
            moving(1.2)
            wait(10)
            print("moving_pid")
            motor_l.run_angle(600, 270, wait=False) #(speed, angle, wait)
            motor_r.run_angle(600, -270, wait=True) #the turning angle depends on your wheels, so choose it to suit yourself
            print("right turning")
            moving(1)
            print("moving_pid")
            rollback()
            wait(10)
        else:
            attempt_count += 1
    else:
        attempt_count = 0 #attempt_count reset: we don't use rollback because can reset all settings

        motor_r.run(600-(error*5))
        motor_l.run(600+(error*5))
    last_error = error

def rollback(): #function to reset all temporary variables 
    global target, error, last_error, attempt_count

    target = 0
    error = 0
    last_error = 0
    attempt_count = 0

last_error = 0
target = 0
error = 0

attempt_count = 0

state = 0

while True:
    dis_f, dis_r, dis_l = get_distances() #this function is not optimised, but now it's OK

    if dis_f <= 90: #distance is in mm so it's 10 cm
        motor_r.hold()
        motor_l.hold() #hold is very strong stop
        wait(100)
        motor_l.run_angle(600, -270, wait=False) #(speed, angle, wait)
        motor_r.run_angle(600, 270, wait=True) #the turning angle depends on your wheels, so choose it to suit yourself
        print("left turning")
        wait(10)
        motor_l.stop()
        motor_r.stop()
        wait(10)
        rollback()
    elif target == 0:
        target = 100 if dis_r == 9999 else dis_r
    else:
        pid()

    wait(10) #wait for high-quality cycle processing
