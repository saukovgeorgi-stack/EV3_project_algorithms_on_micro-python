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

def moving():
    motor_r.run_angle(500, 360, wait=False)
    motor_l.run_angle(500, 360, wait=True)
    motor_l.stop()
    motor_r.stop()

def pid(): #simple PID-controller
    global last_error, error, attempt_count, state, target, dis_r, dis_l

    error = dis_r - target
    if error > last_error + 15 or error < last_error -15 or error > 100:
        if attempt_count > 1:
            moving()
            wait(10)
            print("moving_pid")
            motor_l.run_angle(600, 260, wait=False) #(speed, angle, wait)
            motor_r.run_angle(600, -260, wait=True) #the turning angle depends on your wheels, so choose it to suit yourself
            print("right turning")
            moving()
            print("moving_pid")
            rollback()
            wait(10)
        else:
            attempt_count += 1
    else:
        attempt_count = 0 #attempt_count reset: we don't use rollback because can reset all settings

        motor_r.run(400-(error*4))
        motor_l.run(400+(error*4))
        print("pid", attempt_count)
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

    if dis_f <= 100: #distance is in mm so it's 10 cm
        motor_l.run_angle(400, -300, wait=False) #(speed, angle, wait)
        motor_r.run_angle(400, 300, wait=True) #the turning angle depends on your wheels, so choose it to suit yourself
        print("left turning")
        wait(10)
        motor_l.stop()
        motor_r.stop()
        wait(10)
        rollback()
    elif target == 0:
        target = dis_r
    else:
        pid()

    wait(10) #wait for high-quality cycle processing
