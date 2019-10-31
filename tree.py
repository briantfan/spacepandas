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
    # Go to the tree.
    robot.forward(32, max_speed = -360, decel = 8)
    # Hook the drone
    robot.left_motor.run_angle(-300, 300, Stop.BRAKE)
    # Lower the blocks and move the drone to the ramp.
    robot.right_motor_run_angle(-800, 1100, Stop.BRAKE)
    # Put the drone down.
    robot.left_motor.run_angle(350, 250, Stop.BRAKE)
    robot.left_motor.run_angle(-300, 100, Stop.COAST)
    # Lower the blocks.
    robot.right_motor_run_angle(-800, 900, Stop.COAST)
    robot.left_motor.run_angle(500, 200, Stop.COAST)
    # Back away slowly.
    robot.backward(15, accel=4)
    # Push the right crane lever.
    robot.turn_right(135)
    robot.backward(12)
    # Backup and go home.
    robot.forward(7)
    robot.turn_right(80)
    robot.forward(28)
