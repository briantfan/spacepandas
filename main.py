#!/usr/bin/env pybricks-micropython

from pybricks import ev3brick as brick
from pybricks.parameters import Button
from pybricks.tools import print, wait, StopWatch
import robot

robot = robot.Robot()
brick.sound.beep()

count = 0
stopwatch = StopWatch()
stopwatch.reset()

while True:
#    if stopwatch.time() >= 10000 and stopwatch.time() < 10100:
#        print("10 sec: ", count)
#    count = count + 1

    if Button.UP in brick.buttons():
        robot.move_forward(30)
    elif Button.LEFT in brick.buttons():
        robot.accelerate_forward(30) 
    elif Button.CENTER in brick.buttons():
        robot.accelerate_forward_to_max_speed(40) 
    elif Button.RIGHT in brick.buttons():
        robot.smooth_move_forward(30) 
    elif Button.DOWN in brick.buttons():
        robot.forward(30)
