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

    # This is the increase in speed (per loop) to accelerate.
    ACCELERATION = 10

    def __init__(self):
        self.right_wheel = Motor(Port.B)
        self.left_wheel = Motor(Port.C)
        self.color_sensor_right = ColorSensor(Port.S2)
        self.color_sensor_left = ColorSensor(Port.S3)
        self.gyro_sensor = GyroSensor(Port.S4, Direction.CLOCKWISE)

    def stop(self):
        self.right_wheel.stop(Stop.BRAKE)
        self.left_wheel.stop(Stop.BRAKE)

    def forward(self, inches):
        min_speed = -60
        max_speed = -500
        current_speed = min_speed
        degrees_to_move = inches * self.DEGREES_PER_INCH
        start_wheel_angle = self.left_wheel.angle()
        stop_wheel_angle = start_wheel_angle - degrees_to_move
        slow_wheel_angle = stop_wheel_angle + ((max_speed - min_speed) / self.ACCELERATION)
        if slow_wheel_angle > ((start_wheel_angle + stop_wheel_angle) / 2):
            slow_wheel_angle = (start_wheel_angle + stop_wheel_angle) / 2
        start_gyro_angle = self.gyro_sensor.angle()
        print("Start: ", start_wheel_angle, " Stop: ", stop_wheel_angle, " Slow: ", slow_wheel_angle)
        while self.left_wheel.angle() > stop_wheel_angle:
            if (self.left_wheel.angle() < slow_wheel_angle) and (current_speed < min_speed):
                current_speed = current_speed + self.ACCELERATION
                if current_speed > min_speed:
                    current_speed = min_speed
            elif (current_speed > max_speed):
                current_speed = current_speed - self.ACCELERATION
                if (current_speed < max_speed):
                    current_speed = max_speed
#            print("Angle: ", self.left_wheel.angle(), " current_speed: ", current_speed)
            gyro_error = start_gyro_angle - self.gyro_sensor.angle()
            correction = gyro_error * 100 / current_speed
#            print("Error: ", gyro_error, " Correction: ", correction, " Speed: ", current_speed)
            self.left_wheel.run(current_speed + correction)
            self.right_wheel.run(current_speed - correction)
        self.stop()

    def backward(self, inches):
        min_speed = 60
        max_speed = 500
        current_speed = min_speed
        degrees_to_move = inches * self.DEGREES_PER_INCH
        start_wheel_angle = self.left_wheel.angle()
        stop_wheel_angle = start_wheel_angle + degrees_to_move
        slow_wheel_angle = stop_wheel_angle - ((max_speed - min_speed) / 2)
        if slow_wheel_angle < ((start_wheel_angle + stop_wheel_angle) / 2):
            slow_wheel_angle = (start_wheel_angle + stop_wheel_angle) / 2
        start_gyro_angle = self.gyro_sensor.angle()
        print("Start: ", start_wheel_angle, " Stop: ", stop_wheel_angle, " Slow: ", slow_wheel_angle)
        while self.left_wheel.angle() < stop_wheel_angle:
            if (self.left_wheel.angle() > slow_wheel_angle) and (current_speed > min_speed):
                current_speed = current_speed - self.ACCELERATION
                if current_speed < min_speed:
                    current_speed = min_speed
            elif (current_speed < max_speed):
                current_speed = current_speed + self.ACCELERATION
                if (current_speed > max_speed):
                    current_speed = current_speed
            print("Angle: ", self.left_wheel.angle(), " current_speed: ", current_speed)
            gyro_error = start_gyro_angle - self.gyro_sensor.angle()
            correction = gyro_error * 100 / current_speed
#            print("Error: ", gyro_error, " Correction: ", correction, " Speed: ", current_speed)
            self.right_wheel.run(current_speed - correction)
            self.left_wheel.run(current_speed + correction)
        self.stop()

    def turn_right(self, degrees):
        left_wheel_speed = -120
        right_wheel_speed = 120
        start_angle = self.gyro_sensor.angle()
        stop_angle = start_angle + degrees
        # print("Turn Right ", degrees, " start at ", start_angle, " stop at ", stop_angle)
        while self.gyro_sensor.angle() < stop_angle:
            self.left_wheel.run(left_turning_speed)
            self.right_wheel.run(right_turning_speed)
        self.stop()

    def turn_left(self, degrees):
        left_wheel_speed = 120
        right_wheel_speed = -120
        start_angle = self.gyro_sensor.angle()
        stop_angle = start_angle - degrees
        # print("Turn Left ", degrees, " start at ", start_angle, " stop at ", stop_angle)
        while self.gyro_sensor.angle() > stop_angle:
            self.left_wheel.run(left_wheel_speed)
            self.right_wheel.run(right_wheel_speed)
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
