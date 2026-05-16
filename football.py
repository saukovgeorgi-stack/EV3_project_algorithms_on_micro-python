from pybricks.hubs import EV3Brick
from pybricks.ev3devices import ColorSensor, UltrasonicSensor, GyroSensor, Motor
from pybricks.tools import wait 
from pybricks.parameters import Port, Stop

# initialisation 

cs_1 = ColorSensor(Port. S2)
cs_2 = ColorSensor(Port. S3)

us_f = UltrasonicSensor(Port. S1)

gyro = GyroSensor(Port. S4)

motor_r = Motor(Port. B)
motor_l = Motor(Port. C)

# functions
def reset():
    gyro.reset_angle(0)

def get_sens():
    return cs_1.reflection(), cs_2.reflection(), us_f.distance(), gyro.angle()

first_seen = True
line_following = False
# cicle

reset() 

while True:
    ref1, ref2, dis_f, gyro = get_sens()    

    if first_seen == True:
        if ref1 >= 70:
            motor_r.run_angle(700, 20, wait=False)
            motor_l.run(700, -20, wait=True)
            motor_r.hold()
            motor_l.hold()
            first_seen = False
        else:
            motor_r.run(900)
            motor_l.run(900)