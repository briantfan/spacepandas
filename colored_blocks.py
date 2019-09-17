#!/usr/bin/env pybricks-micropython

from pybricks import ev3brick as brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color,
                                 SoundFile, ImageFile, Align)
from pybricks.tools import print, wait, StopWatch
from pybricks.robotics import DriveBase
import robot

def run(robot):
    robot.forward(12)
    robot.line_follow(12)
    turn.right_wheel(50, max_speed=-50)
    robot.forward(10, max_speed=-90)
    robot.backward(5)
    robot.turn_left(35)
    robot.forward(18.5)
    robot.backward(18.5)
    robot.turn_right(45)
    robot.backward(30)