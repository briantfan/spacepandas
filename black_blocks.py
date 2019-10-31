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
    # Bring the crane attachment down.
    robot.forward(1, min_speed=-1000, max_speed=-1000)
    wait(1000)
    # Move to the crane/circle fast to save time.
    robot.forward(18.8)
    # Push the crane lever slowly and carefully.
    robot.forward(3, max_speed=-100)
    # Wait for the block to fall.
    wait(1000)
    # Move the attachment away so it's not touching the blocks.
    robot.backward(4)
    # Turn and detach from the attachment.
    robot.turn_left(90, min_speed=-200, max_speed=-200)
    # Go back home.
    robot.forward(20, min_speed=-200)
