#!/usr/bin/env pybricks-micropython

from pybricks import ev3brick as brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color,
                                 SoundFile, ImageFile, Align)
from pybricks.tools import print, wait, StopWatch
from pybricks.robotics import DriveBase

class Robot:

    # This is the number of degrees a wheel needs to turn to move one inch.
    DEGREES_PER_INCH = 360 / 11.6

    def __init__(self):
        self.right_wheel = Motor(Port.B)
        self.left_wheel = Motor(Port.C)
        self.color_sensor_right = ColorSensor(Port.S2)
        self.color_sensor_left = ColorSensor(Port.S3)
        self.gyro_sensor = GyroSensor(Port.S4, Direction.CLOCKWISE)
    
    def stop(self):
        self.right_wheel.run(0)
        self.left_wheel.run(0)
    
    def forward(self, inches):
        speed = -160
        degrees_to_move = inches * self.DEGREES_PER_INCH
        start_wheel_angle = self.left_wheel.angle()
        stop_wheel_angle = start_wheel_angle - degrees_to_move
        while self.left_wheel.angle() > stop_wheel_angle:
            gyro_angle = self.gyro_sensor.angle()
            correction = gyro_angle * 10
            self.left_wheel.run(speed + correction)
            self.right_wheel.run(speed - correction)
        self.stop()
    
    def backward(self, inches):
        # do something
        self.stop()

    def turn_right(self, degrees):
        turning_speed = -120
        start_angle = self.gyro_sensor.angle()
        stop_angle = start_angle + degrees
        print("Turn Right ", degrees, " start at ", start_angle, " stop at ", stop_angle)
        while self.gyro_sensor.angle() < stop_angle:
            self.left_wheel.run(turning_speed)
        self.stop()

    def turn_left(self, degrees):
        turning_speed = -120
        start_angle = self.gyro_sensor.angle()
        stop_angle = start_angle - degrees
        print("Turn Left ", degrees, " start at ", start_angle, " stop at ", stop_angle)
        while self.gyro_sensor.angle() > stop_angle:
            self.right_wheel.run(turning_speed)
        self.stop()

    def line_follow(self, inches):
        speed = -160
        degrees_to_move = inches * self.DEGREES_PER_INCH
        start_wheel_angle = self.left_wheel.angle()
        stop_wheel_angle = start_wheel_angle - degrees_to_move
        while self.left_wheel.angle() > stop_wheel_angle:
            right_reflection = self.color_sensor_right.reflection()
            left_reflection = self.color_sensor_left.reflection()
            diff = (right_reflection - left_reflection)
            correction = diff * 4
            self.left_wheel.run(speed + correction)
            self.right_wheel.run(speed - correction)
        self.stop()
