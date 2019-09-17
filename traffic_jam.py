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
    robot.backward(19.25)
    robot.left_motor.run_angle(600, 590, Stop.BRAKE)
    robot.left_motor.run_angle(-600, 150, Stop.BRAKE)
    robot.turn_left(25)
    robot.move_to_line()
    robot.turn_right(220)
    brick.sound.beep()
    robot.ultrasonic_line_follow(985)
    robot.forward(15)