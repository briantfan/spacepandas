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
    robot.forward(32, max_speed = -360, decel = 8) #goes to tree
    robot.left_motor.run_angle(-300, 300, Stop.BRAKE)
    robot.right_motor_run_angle(-800, 1100, Stop.BRAKE)
    robot.left_motor.run_angle(350, 250, Stop.BRAKE) #puts drone down
    robot.left_motor.run_angle(-300, 100, Stop.COAST)
    robot.right_motor_run_angle(-800, 900, Stop.COAST)
    robot.left_motor.run_angle(500, 200, Stop.COAST)
    robot.backward(15, accel = 4)
    robot.turn_right(135)
    robot.backward(10) #goes to crane
    robot.forward(6.5)
    robot.turn_right(80)
    robot.forward(28) #goes home
