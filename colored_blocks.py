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
   # Move to the red circle.
   robot.forward(26)
   # Push the red blocks into the circle.
   robot.turn_left_pivot(45, min_speed=-120)
   robot.turn_right(55)
   # Follow the line a little bit to straighten out.
   robot.line_follow(4, speed=-80)
   # Move to the divot in the line.
   robot.line_follow_to_divot(speed=-60)
   # Turn and move into the tan circle.
   robot.turn_left_absolute(-77, min_speed=-150, max_speed=-150)
   robot.forward(14.5)
   # Back out of the tan circle.
   robot.backward(7)
   # Turn and face the line.
   robot.turn_left_pivot_back(45)
   # Follow the line to the ramp.
   robot.line_follow_to_black()
   # Move up the ramp to the flags.
   robot.backward(2)
   robot.forward(30, decel=10000)