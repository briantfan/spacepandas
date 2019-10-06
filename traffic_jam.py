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
    #pulls up the traffic jam
    robot.left_motor.run_angle(-600, 150, Stop.BRAKE)
    robot.turn_left(25)
    robot.move_to_line()
    robot.turn_right(220)
    robot.line_follow(19, speed=-120)
    robot.line_follow(5.75, speed=-60)
    # knock the bar down on the swing
    robot.turn_left(90)
    robot.forward(9)
    robot.turn_right(80)
    robot.forward(6.25)
    #robot.turn_right(115)
    # knock down two of the six legs holding the tower up
    """
    robot.backward(5.5)
    robot.turn_right(7)
    robot.backward(5.25)
    robot.left_motor.run_angle(-600, 365, Stop.BRAKE)
    robot.turn_left(35)
    robot.backward(5.66)
    # pulls up the tower
    robot.backward(1.25)
    robot.left_motor.run_angle(425, 440, Stop.BRAKE)
    """