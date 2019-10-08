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
   robot.forward (15)
   robot.line_follow (17.5)
   robot.left_motor.run_angle (300, -540)
   robot.line_follow_to_divot()
   robot.turn_left(80, max_speed=-100)
   robot.forward (17)
   robot.backward (9)
   robot.turn_left (25)
   robot.forward (5)
   robot.line_follow_to_end ()
   