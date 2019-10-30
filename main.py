#!/usr/bin/env pybricks-micropython

from pybricks.parameters import (Port, Stop, Direction, Button, Color,
                                 SoundFile, ImageFile, Align)
import time
from pybricks import ev3brick as brick
from pybricks.parameters import Button
from pybricks.tools import print, wait, StopWatch
import robot

import bike
import black_blocks
import colored_blocks
import traffic_jam
import tree
import Crane_Drop

robot = robot.Robot()
stopwatch = StopWatch()

def show_time():
    time = stopwatch.time()
    brick.display.text(time)

while True:
    if Button.UP in brick.buttons():
        stopwatch.reset()
        tree.run(robot)
        robot.right_wheel.stop(Stop.COAST)
        robot.left_wheel.stop(Stop.COAST)
        show_time()
    elif Button.LEFT in brick.buttons():
        stopwatch.reset()
        Crane_Drop.run(robot)
        robot.right_wheel.stop(Stop.COAST)
        robot.left_wheel.stop(Stop.COAST)
        show_time()
    elif Button.CENTER in brick.buttons():
        stopwatch.reset()
        black_blocks.run(robot)
        robot.right_wheel.stop(Stop.COAST)
        robot.left_wheel.stop(Stop.COAST)
        show_time()
    elif Button.RIGHT in brick.buttons():
        stopwatch.reset()
        traffic_jam.run(robot)
        robot.right_wheel.stop(Stop.COAST)
        robot.left_wheel.stop(Stop.COAST)
        show_time()
    elif Button.DOWN in brick.buttons():
        stopwatch.reset()
        colored_blocks.run(robot)
        robot.right_wheel.stop(Stop.BRAKE)
        robot.left_wheel.stop(Stop.BRAKE)
        show_time()

