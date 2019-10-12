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
   robot.forward (17)
   robot.line_follow (16.5)
   # lifting the thing keeping the red blocks with the robot
   robot.left_motor.run_angle (300, -540)
   # getting to the tan circle
   robot.line_follow_to_divot() 
   robot.turn_left(85, max_speed=-100)
   robot.forward (16)
   # backing out of the tan circle
   robot.backward (9.5)
   # getting to the elevator
   robot.turn_right (25)
   robot.forward (3)
   robot.line_follow (10)
   robot.forward (4)
   # getting the elevator to balance
   wait(2000)
   # going up the ramp
   robot.backward (15.5)
   robot.turn_left(85)
   robot.line_follow(10)
   robot.forward (25)