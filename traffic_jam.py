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
    robot.left_motor.run_angle(800, 650)
    robot.left_motor.run_angle(-800, 270)
    # Turn and move toward the line.
    robot.turn_left(25)
    robot.move_to_line_backwards()
    robot.turn_right(220)
    # Keep line following to go up the side of the board.
    robot.line_follow(25, speed=-120)
    # Knock the bar down on the swing and turn towards the bridge.
    robot.turn_left_pivot_back(105, min_speed=-100)
    # Move up to the line.
    robot.forward(8)
    robot.move_to_line(5)
    robot.turn_right(65)
    # Follow the line to flip the elevator.
    robot.line_follow(12)
    robot.line_follow_to_end(2)
    # Goes to do build mission --------------------------
    #robot.backward(5, max_speed=80)
    #robot.backward (6)
    # Sets up to knock down pegs ------------------------
    #robot.turn_left_pivot_back (140)
    #robot.left_motor.run_angle (-800, 315)
    #robot.backward (7)
    # Does Build Mission --------------------------------
    #robot.left_motor.run_angle (-800, 50)
   # robot.turn_right (90)
    # Exits ----------------------------------------------
    #wait (3000) # Wait 3 seconds
    #robot.forward (5)
    #robot.turn_right (55)
   # robot.forward (20, min_speed=200)
    # Goes back to base ----------------------------------
    #robot.forward (20, min_speed=200)
    robot.backward(18, decel=1000)
    robot.turn_right(21, min_speed=120)
    robot.backward(58, min_speed=200, max_speed=800)
