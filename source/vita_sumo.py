from pybricks.hubs import EV3Brick
from pybricks.ev3devices import UltrasonicSensor, Motor
from pybricks.parameters import Stop, Port
from pybricks.tools import wait

ev3 = EV3Brick()

motor_r = Motor(Port. D)
motor_l = Motor(Port. C)

us_f = 1
us_r = 2
us_l = 3

firstly = False
while True:
    ds_f = us_f.distance()
    ds_l = us_l.distance()
    ds_r = us_r.distance()
    
    if firstly == True:
        motor_l.run_angle(1100, 360, wait=False)
        motor_r.run_angle(1100, 360, wait=True)

        if ds_f <= 20:
            firstly = True
        elif ds_r <= 20:
            motor_r.run(-900)
            motor_l.run(900)
            firstly = True
        elif ds_l <= 20:
            motor_r.run(900)
            motor_l.run(-900)
            firstly = True
    
    elif ds_f <= 20:
        motor_r.run(1100)
        motor_l.run(1100)

    else:
        motor_l.run(-900)
        motor_r.run(900)
    
    wait(10)


        

    