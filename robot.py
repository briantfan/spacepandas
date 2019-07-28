#!/usr/bin/env pybricks-micropython

from pybricks import ev3brick as brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color,
                                 SoundFile, ImageFile, Align)
from pybricks.tools import print, wait, StopWatch
from pybricks.robotics import DriveBase

# This is the number of degrees a wheel needs to turn to move one inch.
DEGREES_PER_INCH = 360 / 11.6

# These are the min and max speeds we use for driving and turning.
MIN_FORWARD_SPEED = -50
MAX_FORWARD_SPEED = -500
MIN_BACKWARD_SPEED = 50
MAX_BACKWARD_SPEED = 500
MIN_RIGHT_TURN_SPEED = 50
MAX_RIGHT_TURN_SPEED = 150
MIN_LEFT_TURN_SPEED = -50
MAX_LEFT_TURN_SPEED = -150

class Robot:

    def __init__(self):
        self.right_wheel = Motor(Port.B)
        self.left_wheel = Motor(Port.C)
        self.color_sensor_right = ColorSensor(Port.S2)
        self.color_sensor_left = ColorSensor(Port.S3)
        self.gyro_sensor = GyroSensor(Port.S4, Direction.CLOCKWISE)
        self.check_gyro()

    def check_gyro(self):
        brick.sound.beep()
        gyro_angle = self.gyro_sensor.angle()
        wait(5000)  # wait 5 seconds
        if gyro_angle != self.gyro_sensor.angle():
            brick.sound.beep(400, 500, 30)
            wait(10000)  # wait 10 seconds
        else:
            brick.sound.beep()

    def stop(self):
        self.right_wheel.stop(Stop.BRAKE)
        self.left_wheel.stop(Stop.BRAKE)

    # Make sure our speed is between the min_speed and max_speed
    def check_speed(self, speed, min_speed, max_speed):
        if min_speed < 0:
            # We are moving in the negative direction, so min_speed > max_speed.
            if speed > min_speed:
                return min_speed
            if speed < max_speed:
                return max_speed
        else:
            # We are moving in the positive direction, so min_speed < max_speed.
            if speed < min_speed:
                return min_speed
            if speed > max_speed:
                return max_speed
        return speed
    
    def calculate_run_speed(self, min_speed, max_speed, start_angle, stop_angle, current_angle):
        # The acceleration factor for driving straight is 8.
        # The deceleration factor for driving straight is 2.
        return self.calculate_speed(min_speed, max_speed, start_angle, stop_angle, current_angle, 8, 2)

    def calculate_turn_speed(self, min_speed, max_speed, start_angle, stop_angle, current_angle):
        # The acceleration factor for turning is 8.
        # The deceleration factor for turning is 4.
        return self.calculate_speed(min_speed, max_speed, start_angle, stop_angle, current_angle, 16, 4)

    def calculate_speed(self, min_speed, max_speed, start_angle, stop_angle, current_angle, accel, decel):
        decel_angle = stop_angle - (max_speed / decel)
        middle_angle = (start_angle + stop_angle) / 2
        if min_speed < 0:
            # We are moving in the negative direction, so angles and speed are negative.
            if decel_angle > middle_angle:
                decel_angle = middle_angle
            if current_angle > decel_angle:
                speed = accel * (current_angle - start_angle)
            else:
                speed = decel * (stop_angle - current_angle)
        else:
            # We are moving in the positive direction, so angles and speed are positive.
            if decel_angle < middle_angle:
                decel_angle = middle_angle
            if current_angle < decel_angle:
                speed = accel * (current_angle - start_angle)
            else:
                speed = decel * (stop_angle - current_angle)
        speed = self.check_speed(speed, min_speed, max_speed)
        return speed

    def forward(self, inches):
        degrees_to_move = inches * DEGREES_PER_INCH
        start_wheel_angle = self.left_wheel.angle()
        stop_wheel_angle = start_wheel_angle - degrees_to_move
        print("Inches in Degrees: ", degrees_to_move, "Start: ", start_wheel_angle, " Stop: ", stop_wheel_angle)
        start_gyro_angle = self.gyro_sensor.angle()
        while self.left_wheel.angle() > stop_wheel_angle:
            speed = self.calculate_run_speed(MIN_FORWARD_SPEED, MAX_FORWARD_SPEED, start_wheel_angle, stop_wheel_angle, self.left_wheel.angle())
            gyro_error = start_gyro_angle - self.gyro_sensor.angle()
            correction = gyro_error * 400 / speed
            self.left_wheel.run(speed + correction)
            self.right_wheel.run(speed - correction)
            print("Angle: ", self.left_wheel.angle(), " Speed: ", speed, "Error: ", gyro_error, " Correction: ", correction)
        self.stop()

    def backward(self, inches):
        degrees_to_move = inches * DEGREES_PER_INCH
        start_wheel_angle = self.left_wheel.angle()
        stop_wheel_angle = start_wheel_angle + degrees_to_move
        print("Inches in Degrees: ", degrees_to_move, "Start: ", start_wheel_angle, " Stop: ", stop_wheel_angle)
        start_gyro_angle = self.gyro_sensor.angle()
        while self.left_wheel.angle() < stop_wheel_angle:
            speed = self.calculate_run_speed(MIN_BACKWARD_SPEED, MAX_BACKWARD_SPEED, start_wheel_angle, stop_wheel_angle, self.left_wheel.angle())
            gyro_error = start_gyro_angle - self.gyro_sensor.angle()
            correction = gyro_error * 400 / speed
            self.left_wheel.run(speed - correction)
            self.right_wheel.run(speed + correction)
            print("Angle: ", self.left_wheel.angle(), " Speed: ", speed, "Error: ", gyro_error, " Correction: ", correction)
        self.stop()

    def turn_right(self, degrees):
        start_angle = self.gyro_sensor.angle()
        stop_angle = start_angle + degrees - 1
        print("Turn Right: ", degrees, " Start at: ", start_angle, " Stop at: ", stop_angle)
        while self.gyro_sensor.angle() < stop_angle:
            right_speed = self.calculate_turn_speed(MIN_RIGHT_TURN_SPEED, MAX_RIGHT_TURN_SPEED, start_angle, stop_angle, self.gyro_sensor.angle())
            left_speed = right_speed * -1
            self.right_wheel.run(right_speed)
            self.left_wheel.run(left_speed)
            print("Angle: ", self.gyro_sensor.angle())
        self.stop()

    def turn_left(self, degrees):
        start_angle = self.gyro_sensor.angle()
        stop_angle = start_angle - degrees + 1
        print("Turn Left: ", degrees, " Start at: ", start_angle, " Stop at: ", stop_angle)
        while self.gyro_sensor.angle() > stop_angle:
            right_speed = self.calculate_turn_speed(MIN_LEFT_TURN_SPEED, MAX_LEFT_TURN_SPEED, start_angle, stop_angle, self.gyro_sensor.angle())
            left_speed = right_speed * -1
            self.right_wheel.run(right_speed)
            self.left_wheel.run(left_speed)
            print("Angle: ", self.gyro_sensor.angle())
        self.stop()

    def line_follow(self, inches):
        speed = -160
        degrees_to_move = inches * DEGREES_PER_INCH
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
        degrees_to_move = inches * DEGREES_PER_INCH
        self.left_wheel.run_angle(speed, degrees_to_move, Stop.BRAKE, False)
        self.right_wheel.run_angle(speed, degrees_to_move, Stop.BRAKE, True)

    def accelerate_forward(self, inches):
        speed = -10
        degrees_to_move = inches * DEGREES_PER_INCH
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
        speed = -10
        max_speed = -400
        degrees_to_move = inches * DEGREES_PER_INCH
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
        min_speed = -50
        max_speed = -500
        degrees_to_move = inches * DEGREES_PER_INCH
        start_wheel_angle = self.left_wheel.angle()
        stop_wheel_angle = start_wheel_angle - degrees_to_move
        print("Degrees: ", degrees_to_move, "Start: ", start_wheel_angle, " Stop: ", stop_wheel_angle)
        while self.left_wheel.angle() > stop_wheel_angle:
            speed = self.calculate_speed(min_speed, max_speed, start_wheel_angle, stop_wheel_angle, self.left_wheel.angle())
            self.left_wheel.run(speed)
            self.right_wheel.run(speed)
            print("Angle: ", self.left_wheel.angle(), " Speed: ", speed)
        self.stop()
