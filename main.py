#!/usr/bin/env pybricks-micropython

from pybricks import ev3brick as brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color,
                                 SoundFile, ImageFile, Align)
from pybricks.tools import print, wait, StopWatch
from pybricks.robotics import DriveBase
import time

# Get all of our code for our runs.
import robot
import black_blocks
import colored_blocks
import traffic_jam
import tree
import Crane_Drop

# Initialize the robot.
robot = robot.Robot()
# Initialize the stopwatch.
stopwatch = StopWatch()

# Make a function to time our runs to see how we're doing.
def show_time():
    time = stopwatch.time()
    brick.display.text(time)

# Master program loop.
while True:
    if Button.UP in brick.buttons():
        # First: tree run
        stopwatch.reset()
        tree.run(robot)
        robot.right_wheel.stop(Stop.COAST)
        robot.left_wheel.stop(Stop.COAST)
        show_time()
    elif Button.LEFT in brick.buttons():
        # Second: crane run
        stopwatch.reset()
        Crane_Drop.run(robot)
        robot.right_wheel.stop(Stop.COAST)
        robot.left_wheel.stop(Stop.COAST)
        show_time()
    elif Button.CENTER in brick.buttons():
        # Third: black blocks run
        stopwatch.reset()
        black_blocks.run(robot)
        robot.right_wheel.stop(Stop.COAST)
        robot.left_wheel.stop(Stop.COAST)
        show_time()
    elif Button.RIGHT in brick.buttons():
        # Fourth: traffic jam run
        stopwatch.reset()
        traffic_jam.run(robot)
        robot.right_wheel.stop(Stop.COAST)
        robot.left_wheel.stop(Stop.COAST)
        show_time()
    elif Button.DOWN in brick.buttons():
        # Fifth: colored blocks run
        stopwatch.reset()
        colored_blocks.run(robot)
        robot.right_wheel.stop(Stop.BRAKE)
        robot.left_wheel.stop(Stop.BRAKE)
        show_time()
