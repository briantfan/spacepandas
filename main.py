#!/usr/bin/env pybricks-micropython

from pybricks import ev3brick as brick
from pybricks.parameters import Button
from pybricks.tools import print, wait, StopWatch
import robot

robot = robot.Robot()
stopwatch = StopWatch()
stopwatch.reset()

time = stopwatch.time()
brick.display.text(time)

count = 0
while True:
#    if stopwatch.time() >= 10000 and stopwatch.time() < 10100:
#        print("10 sec: ", count)
#    count = count + 1

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

"""
    if Button.UP in brick.buttons():
        start_angle = robot.gyro_sensor.angle()
        robot.move_forward(50)
        brick.display.text(robot.gyro_sensor.angle() - start_angle)
    elif Button.LEFT in brick.buttons():
        start_angle = robot.gyro_sensor.angle()
        robot.accelerate_forward(30) 
        brick.display.text(robot.gyro_sensor.angle() - start_angle)
    elif Button.CENTER in brick.buttons():
        start_angle = robot.gyro_sensor.angle()
        robot.accelerate_forward_to_max_speed(40) 
        brick.display.text(robot.gyro_sensor.angle() - start_angle)
    elif Button.RIGHT in brick.buttons():
        start_angle = robot.gyro_sensor.angle()
        robot.smooth_move_forward(30) 
        brick.display.text(robot.gyro_sensor.angle() - start_angle)
    elif Button.DOWN in brick.buttons():
        start_angle = robot.gyro_sensor.angle()
        robot.forward(30)
        brick.display.text(robot.gyro_sensor.angle() - start_angle)
"""