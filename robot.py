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
        self.right_wheel.stop(Stop.BRAKE)
        self.left_wheel.stop(Stop.BRAKE)

    def check_speed(self, speed, min_speed, max_speed):
        if min_speed < 0:
            # We are moving in the negative direction.
            if speed > min_speed:
                return min_speed
            if speed < max_speed:
                return max_speed
        else:
            # We are moving in the positive direction.
            if speed < min_speed:
                return min_speed
            if speed > max_speed:
                return max_speed
        return speed
    
    def calculate_speed(self, min_speed, max_speed, start_angle, stop_angle, current_angle):
        slow_angle = stop_angle - max_speed
        middle_angle = (start_angle + stop_angle) / 2
        if min_speed < 0:
            # We are moving in the negative direction.
            if slow_angle > middle_angle:
                slow_angle = middle_angle
            if current_angle > slow_angle:
                speed = current_angle - start_angle
            else:
                speed = stop_angle - current_angle
        else:
            # We are moving in the positive direction.
            if slow_angle < middle_angle:
                slow_angle = middle_angle
            if current_angle < slow_angle:
                speed = current_angle - start_angle
            else:
                speed = stop_angle - current_angle
        speed = self.check_speed(speed, min_speed, max_speed)
        return speed

    def forward(self, inches):
        min_speed = -100
        max_speed = -500
        degrees_to_move = inches * self.DEGREES_PER_INCH
        start_wheel_angle = self.left_wheel.angle()
        stop_wheel_angle = start_wheel_angle - degrees_to_move
        print("Degrees: ", degrees_to_move, "Start: ", start_wheel_angle, " Stop: ", stop_wheel_angle)
        start_gyro_angle = self.gyro_sensor.angle()
        while self.left_wheel.angle() > stop_wheel_angle:
            speed = self.calculate_speed(min_speed, max_speed, start_wheel_angle, stop_wheel_angle, self.left_wheel.angle())
            gyro_error = start_gyro_angle - self.gyro_sensor.angle()
            correction = gyro_error * 50 / speed
            self.left_wheel.run(speed + correction)
            self.right_wheel.run(speed - correction)
            print("Angle: ", self.left_wheel.angle(), " Speed: ", speed, "Error: ", gyro_error, " Correction: ", correction)
        self.stop()

    def backward(self, inches):
        min_speed = 100
        max_speed = 500
        degrees_to_move = inches * self.DEGREES_PER_INCH
        start_wheel_angle = self.left_wheel.angle()
        stop_wheel_angle = start_wheel_angle + degrees_to_move
        print("Degrees: ", degrees_to_move, "Start: ", start_wheel_angle, " Stop: ", stop_wheel_angle)
        start_gyro_angle = self.gyro_sensor.angle()
        while self.left_wheel.angle() < stop_wheel_angle:
            speed = self.calculate_speed(min_speed, max_speed, start_wheel_angle, stop_wheel_angle, self.left_wheel.angle())
            gyro_error = start_gyro_angle - self.gyro_sensor.angle()
            correction = gyro_error * 100 / current_speed
            self.right_wheel.run(current_speed - correction)
            self.left_wheel.run(current_speed + correction)
            print("Angle: ", self.left_wheel.angle(), " Speed: ", speed, "Error: ", gyro_error, " Correction: ", correction)
        self.stop()

    def turn_right(self, degrees):
        left_wheel_speed = -120
        right_wheel_speed = 120
        start_angle = self.gyro_sensor.angle()
        stop_angle = start_angle + degrees
        print("Turn Right: ", degrees, " Start at: ", start_angle, " Stop at: ", stop_angle)
        while self.gyro_sensor.angle() < stop_angle:
            self.left_wheel.run(left_turning_speed)
            self.right_wheel.run(right_turning_speed)
            print("Angle: ", self.gyro_sensor.angle())
        self.stop()

    def turn_left(self, degrees):
        left_wheel_speed = 120
        right_wheel_speed = -120
        start_angle = self.gyro_sensor.angle()
        stop_angle = start_angle - degrees
        print("Turn Right: ", degrees, " Start at: ", start_angle, " Stop at: ", stop_angle)
        while self.gyro_sensor.angle() > stop_angle:
            self.left_wheel.run(left_wheel_speed)
            self.right_wheel.run(right_wheel_speed)
            print("Angle: ", self.gyro_sensor.angle())
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

    def move_forward(self, inches):
        speed = -500
        degrees_to_move = inches * self.DEGREES_PER_INCH
        self.left_wheel.run_angle(speed, degrees_to_move, Stop.BRAKE, False)
        self.right_wheel.run_angle(speed, degrees_to_move, Stop.BRAKE, True)

    def accelerate_forward(self, inches):
        speed = 0
        degrees_to_move = inches * self.DEGREES_PER_INCH
        start_wheel_angle = self.left_wheel.angle()
        stop_wheel_angle = start_wheel_angle - degrees_to_move
        print("Degrees: ", degrees_to_move, "Start: ", start_wheel_angle, " Stop: ", stop_wheel_angle)
        while self.left_wheel.angle() > stop_wheel_angle:
            speed = speed - 10
            self.left_wheel.run(speed)
            self.right_wheel.run(speed)
            print("Angle: ", self.left_wheel.angle(), " Speed: ", speed)
        self.stop()

    def accelerate_forward_to_max_speed(self, inches):
        speed = 0
        max_speed = -400
        degrees_to_move = inches * self.DEGREES_PER_INCH
        start_wheel_angle = self.left_wheel.angle()
        stop_wheel_angle = start_wheel_angle - degrees_to_move
        print("Degrees: ", degrees_to_move, "Start: ", start_wheel_angle, " Stop: ", stop_wheel_angle)
        while self.left_wheel.angle() > stop_wheel_angle:
            speed = speed - 10
            if speed < max_speed:
                speed = max_speed
            self.left_wheel.run(speed)
            self.right_wheel.run(speed)
            print("Angle: ", self.left_wheel.angle(), " Speed: ", speed)
        self.stop()

    def smooth_move_forward(self, inches):
        min_speed = -100
        max_speed = -500
        degrees_to_move = inches * self.DEGREES_PER_INCH
        start_wheel_angle = self.left_wheel.angle()
        stop_wheel_angle = start_wheel_angle - degrees_to_move
        print("Degrees: ", degrees_to_move, "Start: ", start_wheel_angle, " Stop: ", stop_wheel_angle)
        while self.left_wheel.angle() > stop_wheel_angle:
            speed = self.calculate_speed(min_speed, max_speed, start_wheel_angle, stop_wheel_angle, self.left_wheel.angle())
            self.left_wheel.run(speed)
            self.right_wheel.run(speed)
            print("Angle: ", self.left_wheel.angle(), " Speed: ", speed)
        self.stop()
