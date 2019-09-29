#!/usr/bin/env pybricks-micropython

import time
from pybricks import ev3brick as brick
from pybricks.parameters import Button
from pybricks.tools import print, wait, StopWatch
import robot

import bike
import traffic_jam
import tree
import colored_blocks
robot = robot.Robot()
stopwatch = StopWatch()
stopwatch.reset()

colored_blocks.run (robot)
#traffic_jam.run(robot)
#tree.run(robot)

time = stopwatch.time()
brick.display.text(time)

count = 0

while False:
    if Button.UP in brick.buttons():
        start_angle = robot.gyro_sensor.angle()
        robot.backward(30)
        brick.display.text(robot.gyro_sensor.angle() - start_angle)
    elif Button.LEFT in brick.buttons():
        start_angle = robot.gyro_sensor.angle()
        robot.turn_right(90)
        brick.display.text(robot.gyro_sensor.angle() - start_angle)
    elif Button.CENTER in brick.buttons():
        robot.line_follow(20)
    elif Button.RIGHT in brick.buttons():
        start_angle = robot.gyro_sensor.angle()
        robot.turn_left(90)
        brick.display.text(robot.gyro_sensor.angle() - start_angle)
    elif Button.DOWN in brick.buttons():
        start_angle = robot.gyro_sensor.angle()
        robot.forward(30)
        brick.display.text(robot.gyro_sensor.angle() - start_angle)

