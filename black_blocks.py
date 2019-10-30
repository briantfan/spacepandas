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
    robot.forward(1, min_speed=-1000, max_speed=-1000)
    wait(1000)
    robot.forward(18.8)
    robot.forward(3, max_speed=-100)
    wait(1000)
    robot.backward(4)
    robot.turn_left(90, min_speed=-200, max_speed=-200)
    robot.forward(20, min_speed=-200)