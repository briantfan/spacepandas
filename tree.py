#!/usr/bin/env pybricks-micropython

import time
from pybricks import ev3brick as brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color,
                                 SoundFile, ImageFile, Align)
from pybricks.tools import print, wait, StopWatch
from pybricks.robotics import DriveBase
import robot

def run(robot):
    robot.forward(32)
    for i in range(100):
        robot.left_wheel.run(-50 - i)
    robot.left_wheel.stop(Stop.BRAKE)
    robot.left_motor.run_angle(-400, 270, Stop.BRAKE)
    robot.right_motor.run_angle(-400, 1140, Stop.BRAKE)
    robot.left_motor.run_angle(500, 160, Stop.BRAKE)
    robot.right_motor.run_angle(400, 250, Stop.BRAKE)
    robot.left_motor.run_angle(500, 90, Stop.COAST)
    robot.right_motor.run_angle(-500, 850, Stop.COAST)
    time.sleep(1)
    robot.backward(4)
