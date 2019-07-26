#!/usr/bin/env pybricks-micropython

from pybricks import ev3brick as brick
from pybricks.parameters import Button
from pybricks.tools import print, wait, StopWatch
import robot

robot = robot.Robot()
brick.sound.beep()
"""
robot.line_follow(50)
robot.turn_left(90)
robot.line_follow(19)
robot.turn_left(90)
robot.forward(33)
robot.turn_left(90)
robot.forward(12)
robot.turn_right(90)
robot.line_follow(19)
"""

count = 0
stopwatch = StopWatch()
stopwatch.reset()
while True:
#    if stopwatch.time() >= 10000:
#        print("10 sec: ", count)
#    count = count + 1
    if Button.DOWN in brick.buttons():
        robot.forward(40) 
    elif Button.UP in brick.buttons():
        robot.backward(40)
    elif Button.LEFT in brick.buttons():
        robot.turn_right(90)
    elif Button.RIGHT in brick.buttons():
        robot.turnLeft(90)
    elif Button.CENTER in brick.buttons():
        robot.line_follow(50)
