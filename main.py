#!/usr/bin/env pybricks-micropython

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
    stopwatch.reset()
    if Button.UP in brick.buttons():
        tree.run(robot)
        show_time()
    elif Button.LEFT in brick.buttons():
        Crane_Drop.run(robot)
        show_time()
    elif Button.CENTER in brick.buttons():
        black_blocks.run(robot)
        show_time()
    elif Button.RIGHT in brick.buttons():
        traffic_jam.run(robot)
        show_time()
    elif Button.DOWN in brick.buttons():
        colored_blocks.run(robot)
        show_time()
