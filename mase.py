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
    if error > last_error + 10 or error < last_error -10:
        moving()
        print("moving_pid")
        motor_l.run_angle(600, 250, wait=False) #(speed, angle, wait)
        motor_r.run_angle(600, -250, wait=True) #the turning angle depends on your wheels, so choose it to suit yourself
        print("right turning")
        moving()
        print("moving_pid")
        target = 0
        state = 1 #this is our break, because utside the loop we can't use simple break
    else:
        motor_r.run(target)
        motor_l.run(target)
        print("pid")
    last_error = error
last_error = 0
target = 0
error = 0
state = 0

while True:
    dis_f, dis_r, dis_l = get_distances() #this function is not optimised, but now it's OK

    if state == 1:
        break
    elif dis_f < 150: #distance is in mm so it's 15 cm
        motor_l.run_angle(600, -250, wait=False) #(speed, angle, wait)
        motor_r.run_angle(600, 250, wait=True) #the turning angle depends on your wheels, so choose it to suit yourself
        print("left turning")
        break
    elif target == 0:
        target = dis_r
    elif dis_r < target-2 or dis_r > target+2:
        pid()
    else:
        motor_r.run(500)
        motor_l.run(500)
        print("moving")

    wait(10) #wait for high-quality cycle processing
print(target)
