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
    robot.backward2(19.5)
    # Pull up the traffic jam.
    robot.left_motor.run_angle(800, 650)
    robot.left_motor.run_angle(-800, 270)
    # Turn and move toward the line.
    robot.turn_left(25)
    robot.move_to_line_backwards()
    robot.turn_right(220, min_speed=80)
    # Keep line following to go up the side of the board.
    robot.line_follow(23, speed=-150)
    robot.gyro_sensor.reset_angle(0)
    robot.line_follow2(2, speed=-150)
    # Knock the bar down on the swing and turn towards the bridge.
    robot.turn_left_absolute2(-100, min_speed=180)
    # Move up to the line.
    robot.forward(8)
    robot.move_to_line(5)
    robot.turn_right(65)
    # Follow the line to flip the elevator.
    robot.line_follow(10)
    brick.sound.beep()
    robot.forward(2)
    # Goes to do build mission
    robot.backward(5, max_speed=80, gyro_correct=0)
    robot.backward(6, gyro_correct=0)
    # Sets up to knock down two blue pegs
    robot.left_motor.run_angle(-800, 315, Stop.BRAKE, False)
    robot.turn_left_pivot_back(142, min_speed=-180)
    robot.backward_or_wait(7, 2000)
    # Does Build Mission
    robot.left_motor.run_angle(-800, 80)
    robot.turn_right(90)
  # Goes back to base
    robot.left_motor.run_angle(800, 500, Stop.BRAKE, False)
    robot.turn_left_pivot(98, min_speed=-180) #94
    robot.forward(72)
