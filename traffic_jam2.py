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
    robot.backward(1)
    robot.turn_right(102)
    robot.backward(10.75)
    robot.turn_left(4.12)
    robot.left_motor.run_angle(-600, 365, Stop.BRAKE)
    robot.backward(5.5)
    robot.left_motor.run_angle(405, 440, Stop.BRAKE)
    robot.forward(10.5)
    robot.turn_left(105)
    robot.backward(72)
   
    

