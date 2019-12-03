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
    # Bring in the tower and blocks.
    robot.forward(1, min_speed=-1000, max_speed=-1000)
    wait(1000)
    # Move to the crane/circle fast to save time.
    robot.forward(20)
    # Push the crane lever slowly and carefully.
    robot.forward(1, max_speed=-120)
    # Wait for the block to fall.
    wait(1000)
    # Move the attachment away so it's not touching the blocks.
    robot.backward(4)
    # Turn and detach from the attachment.
    robot.turn_right(10)
    robot.turn_left_pivot_back(110, min_speed=-200, max_speed=-400)
    # Go back home.
    robot.forward(20, min_speed=-600)
