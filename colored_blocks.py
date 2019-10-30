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
   
   # getting to the red circle
   robot.forward(27)
   # lifting the thing keeping the red blocks with the robot
   robot.turn_left_pivot(45, min_speed=-150)
   robot.turn_right(55)
   robot.line_follow(4, speed=-80)
   # getting to the tan circle
   robot.line_follow_to_divot(speed=-60)
   robot.turn_left_absolute(-77, min_speed=-150, max_speed=-150)
   robot.forward(14.5)
   # backing out of the tan circle
   robot.backward(7)
   robot.turn_left_pivot_back(45)
   # going up the ramp
   robot.line_follow_to_black()
   robot.forward(28, max_speed=-300)