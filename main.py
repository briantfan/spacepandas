#!/usr/bin/env pybricks-micropython

import time
from pybricks import ev3brick as brick
from pybricks.parameters import Button
from pybricks.tools import print, wait, StopWatch
import robot

import bike
import traffic_jam
import tree
import Crane_Drop
import black_blocks

robot = robot.Robot()
stopwatch = StopWatch()
stopwatch.reset()

#time = stopwatch.time()
#brick.display.text(time)

while True:
    if Button.UP in brick.buttons():
        tree.run(robot)
    elif Button.LEFT in brick.buttons():
        Crane_Drop.run(robot)
    elif Button.CENTER in brick.buttons():
        black_blocks.run(robot)
    elif Button.RIGHT in brick.buttons():
        pass
    elif Button.DOWN in brick.buttons():
       pass
