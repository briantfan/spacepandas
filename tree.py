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
    robot.forward(35, max_speed=-360, decel=8)
    # Hook the drone
    robot.left_motor.run_angle(400, 360)
    # Lower the blocks and move the drone to the ramp.
    robot.right_motor.run_angle(-400, 1000)
    # Put the drone down.
    robot.left_motor.run_angle(-400, 900)
    # Lower the blocks.
    robot.right_motor.run_angle(-400, 500)
    # Back away slowly.
    robot.backward(15, accel=4)
    # Push the right crane lever.
    robot.turn_right(136)
    robot.backward(10, decel=4)
    robot.backward(1)
    # Backup and go home.
    robot.forward(7)
    robot.turn_right(80)
    robot.forward(28)
