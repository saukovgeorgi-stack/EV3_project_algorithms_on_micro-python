#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, UltrasonicSensor
from pybricks.parameters import Port, Stop
from pybricks.tools import wait

# Инициализация
ev3 = EV3Brick()

motor_r = Motor(Port.B)
motor_l = Motor(Port.C)

us_front = UltrasonicSensor(Port.S3)
us_left  = UltrasonicSensor(Port.S4) 
us_right = UltrasonicSensor(Port.S2) 

# константы
MAX_POWER = 1700        
SEARCH_POWER = 1100       
DETECT_DIST_F = 700     # 70 см
DETECT_DIST_SIDE = 550  # 55 см
DOVOROT_MOTOR_DEG = 100 

motor_l.control.limits(acceleration=10000) 
motor_r.control.limits(acceleration=10000)

# флаги состояния
first_encounter = True
last_turn_dir = 0  

wait(500)
while True:
    # 1.считываем только передний датчик 
    dist_f = us_front.distance()
    dist_l = us_left.distance()
    dist_r = us_right.distance()

    if dist_f < DETECT_DIST_F:
        if first_encounter == True:
            motor_l.hold()
            motor_r.hold()
            wait(50)
            
            if last_turn_dir == 1:
                motor_l.run_angle(1400, DOVOROT_MOTOR_DEG, wait=False)
                motor_r.run_angle(1400, -DOVOROT_MOTOR_DEG, wait=True)
            elif last_turn_dir == -1:
                motor_l.run_angle(1400, -DOVOROT_MOTOR_DEG, wait=False)
                motor_r.run_angle(1400, DOVOROT_MOTOR_DEG, wait=True)
            
            first_encounter = False

        # аткуем
        if dist_f < 200:
            motor_l.run(1100)
            motor_r.run(1100)

    else:
        #2.противника спереди нет, считаем левый датчик.
        
        if dist_l < DETECT_DIST_SIDE:
            last_turn_dir = -1
            motor_l.run(-MAX_POWER)
            motor_r.run(MAX_POWER)
        
        else:
            # 3.противника слева нет, считаем правый датчик.
            
            
            if dist_r < DETECT_DIST_SIDE:
                last_turn_dir = 1
                motor_l.run(MAX_POWER)
                motor_r.run(-MAX_POWER)
            
            else:
                # 4.вообще никого нет, поиск
                if last_turn_dir == -1:
                    motor_l.run(-SEARCH_POWER)
                    motor_r.run(SEARCH_POWER)
                else:
                    last_turn_dir = 1
                    motor_l.run(SEARCH_POWER)
                    motor_r.run(-SEARCH_POWER)
