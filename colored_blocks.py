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
   robot.line_follow(6, speed=-80)
   # Move to the divot in the line.
   robot.line_follow_to_divot(speed=-60)
   # Turn and move into the tan circle.
   robot.turn_left_absolute(-77, min_speed=-100, max_speed=-100)
   robot.forward(14.5)
   # Back out of the tan circle.
   robot.backward(7)
   # Turn and face the line.
   robot.turn_left_pivot_back(45)
  # Follow the line to the ramp.
   robot.line_follow (4)
   robot.line_follow_to_black()
   # Move up the ramp to the flags.
   robot.forward(25, decel=10000)
   robot.left_motor.set_pid_settings(100, 50, 1, 1000, 50, 50, 0, 1000)
   robot.left_motor.run_angle(-800, 850,Stop.BRAKE, False)
   robot.right_motor.run_angle(800, 850)
