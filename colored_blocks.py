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
    robot.forward(14.5)
    robot.line_follow(7)
    robot.right_wheel.run_angle(100, -110, Stop.BRAKE)
    robot.forward(4)
    brick.sound.beep()
    robot.turn_right(80)
    robot.forward(4.5)
    robot.turn_left(70)
    robot.forward(14.5)
    robot.turn_left(34.4)
    robot.forward(7.5)
    robot.backward(6.5)
    robot.turn_left(40)
    robot.line_follow(10)
    brick.sound.beep()
    robot.forward(29, max_speed = -500) 
