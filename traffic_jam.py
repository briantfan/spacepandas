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
    # Move to the traffic jam.
    robot.backward(19.25)
    # Pull up the traffic jam.
    robot.left_motor.run_angle(600, 590, Stop.BRAKE)
    robot.left_motor.run_angle(-600, 150, Stop.BRAKE)
    # Turn and move toward the line.
    robot.turn_left(25)
    robot.move_to_line()
    robot.turn_right(220)
    # Keep line following to go up the side of the board.
    robot.line_follow(24, speed=-120)
    # Knock the bar down on the swing.
    robot.backward(2)
    robot.turn_right(90)
    robot.backward(10.5)
    robot.turn_left(90)
    # Square up to the tower.
    robot.forward(14)
    # Move to the steel construction.
    robot.right_wheel.run_angle(100, 285)
    robot.backward(6)
    robot.left_wheel.run_angle(100, 65)
    # Raise the tower.
    robot.left_motor.run_angle(-600, 365, Stop.BRAKE)
    # Drive around the elevator.
    robot.backward(3.18)
    robot.left_motor.run_angle(405, 440, Stop.BRAKE)
    robot.forward(10)
    robot.turn_left(105)
    # Go home
    robot.backward(72)
