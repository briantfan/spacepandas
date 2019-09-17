#!/usr/bin/env pybricks-micropython

from pybricks import ev3brick as brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color,
                                 SoundFile, ImageFile, Align)
from pybricks.tools import print, wait, StopWatch
from pybricks.robotics import DriveBase
import time
import robot

def run(robot):
    robot.backward(31.8)
    time.sleep(1)
    robot.forward(12.1)
    #robot.turn_right(90)
    robot.right_wheel.run_angle(200,110,Stop.BRAKE,False)
    robot.left_wheel.run_angle(-200,110,Stop.BRAKE)
    robot.forward(19.5)