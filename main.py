#!/usr/bin/env pybricks-micropython

from pybricks import ev3brick as brick
from pybricks.parameters import Button
import robot

robot = robot.Robot()
brick.sound.beep()
while True:
    if Button.DOWN in brick.buttons():
        robot.forward(10) 
    elif Button.LEFT in brick.buttons():
        robot.turnRight(90)
    elif Button.RIGHT in brick.buttons():
        robot.turnLeft(90)
    elif Button.CENTER in brick.buttons():
        robot.line_follow(20)
