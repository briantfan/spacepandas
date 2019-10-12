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
    robot.line_follow(24, speed=-120)
    # knock the bar down on the swing
    robot.backward(2)
    robot.turn_right(90)
    robot.backward(10.5)
    robot.turn_left(90)
    robot.forward(14)
    #squares up to the tower
    #robot.backward(1)
    robot.right_wheel.run_angle(100, 285)
    wait(2000)
    #robot.turn_right(102)
    robot.backward(6)
    robot.left_wheel.run_angle(100, 65)
    robot.left_motor.run_angle(-600, 365, Stop.BRAKE)
    robot.backward(3.18)
    robot.left_motor.run_angle(405, 440, Stop.BRAKE)
    robot.forward(10)
    robot.turn_left(105)
    robot.backward(72)
   
