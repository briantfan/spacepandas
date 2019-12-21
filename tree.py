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
    # Go to the tree.
    robot.forward2(37, 3000, max_speed=-400, gyro_correct=1500)
    robot.right_wheel.run_angle(-300, 90)
    robot.right_wheel.stop()
    robot.left_wheel.run_angle(-300, 90)
    robot.left_wheel.stop()
    # Hook the drone
    robot.right_motor.run_angle(-1000, 650, Stop.BRAKE, False)
    robot.left_motor.run_angle(500, 1100)
    # Lower the blocks.
    robot.right_motor.run_angle(-1000, 850)
    # Back away.
    robot.backward(12, accel=8)
    # Push the right crane lever.
    robot.turn_right(45)
    robot.backward(4)
    robot.turn_right(88)
    robot.backward_or_wait(8.5, 2000)
    robot.backward_or_wait(2, 1000, min_speed=120, max_speed=120)
    # Backup and go home.
    robot.drive_right(90, -600, -400)
    robot.forward(17, min_speed=-600, max_speed=-600)

