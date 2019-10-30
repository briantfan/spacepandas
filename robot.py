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
MIN_FORWARD_SPEED = -60
MAX_FORWARD_SPEED = -500
MIN_BACKWARD_SPEED = 60
MAX_BACKWARD_SPEED = 500

DEFAULT_MOVE_ACCELERATION = 16
DEFAULT_MOVE_DECELERATION = 32

MIN_RIGHT_TURN_SPEED = 60
MAX_RIGHT_TURN_SPEED = 150
MIN_LEFT_TURN_SPEED = -60
MAX_LEFT_TURN_SPEED = -150

DEFAULT_TURN_ACCELERATION = 16
DEFAULT_TURN_DECELERATION = 16

LINE_FOLLOW_SPEED = -150
GYRO_CORRECTION = 800

class Robot:

    def __init__(self):
        self.right_wheel = Motor(Port.B)
        self.left_wheel = Motor(Port.C)
        self.left_motor = Motor(Port.D)
        self.right_motor = Motor(Port.A)
        self.color_sensor_right = ColorSensor(Port.S2)
        self.color_sensor_left = ColorSensor(Port.S3)
        self.gyro_sensor = GyroSensor(Port.S4, Direction.CLOCKWISE)
        self.check_gyro()
        
    def check_gyro(self):
        brick.sound.beep()
        gyro_angle = self.gyro_sensor.angle()
        wait(2000)  # wait 5 seconds
        if gyro_angle != self.gyro_sensor.angle():
            brick.sound.beep(400, 500, 30)
            wait(5000)  # wait 5 seconds
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
    
    def calculate_speed(self, min_speed, max_speed, current_speed, start_angle, stop_angle, current_angle, accel, decel):
        decel_angle = stop_angle - ((current_speed - min_speed) / (decel / accel))
        middle_angle = (start_angle + stop_angle) / 2
        if min_speed < 0:
            # We are moving in the negative direction, so angles and speed are negative.
            if decel_angle > middle_angle:
                decel_angle = middle_angle
            if current_angle > decel_angle:
                speed = current_speed - accel
            else:
                speed = current_speed + decel
        else:
            # We are moving in the positive direction, so angles and speed are positive.
            if decel_angle < middle_angle:
                decel_angle = middle_angle
            if current_angle < decel_angle:
                speed = current_speed + accel
            else:
                speed = current_speed - decel
        speed = self.check_speed(speed, min_speed, max_speed)
        return speed

    def forward(self, inches, min_speed=MIN_FORWARD_SPEED, max_speed=MAX_FORWARD_SPEED, accel=DEFAULT_MOVE_ACCELERATION, decel=DEFAULT_MOVE_DECELERATION, gyro_correct=GYRO_CORRECTION):
        degrees_to_move = inches * DEGREES_PER_INCH
        start_angle = self.left_wheel.angle()
        stop_angle = start_angle - degrees_to_move
        print("Inches in Degrees: ", degrees_to_move, "Start: ", start_angle, " Stop: ", stop_angle)
        start_gyro_angle = self.gyro_sensor.angle()
        current_speed = min_speed
        while self.left_wheel.angle() > stop_angle:
            current_speed = self.calculate_speed(min_speed, max_speed, current_speed, start_angle, stop_angle, self.left_wheel.angle(), accel, decel)
            gyro_error = start_gyro_angle - self.gyro_sensor.angle()
            correction = gyro_error * gyro_correct / current_speed
            self.left_wheel.run(current_speed + correction)
            self.right_wheel.run(current_speed - correction)
            print("Angle: ", self.left_wheel.angle(), " Speed: ", current_speed, "Error: ", gyro_error, " Correction: ", correction)
        self.stop()

    def backward(self, inches, min_speed=MIN_BACKWARD_SPEED, max_speed=MAX_BACKWARD_SPEED, accel=DEFAULT_MOVE_ACCELERATION, decel=DEFAULT_MOVE_DECELERATION, gyro_correct=GYRO_CORRECTION):
        degrees_to_move = inches * DEGREES_PER_INCH
        start_angle = self.left_wheel.angle()
        stop_angle = start_angle + degrees_to_move
        print("Inches in Degrees: ", degrees_to_move, "Start: ", start_angle, " Stop: ", stop_angle)
        start_gyro_angle = self.gyro_sensor.angle()
        current_speed = min_speed
        while self.left_wheel.angle() < stop_angle:
            current_speed = self.calculate_speed(min_speed, max_speed, current_speed, start_angle, stop_angle, self.left_wheel.angle(), accel, decel)
            gyro_error = start_gyro_angle - self.gyro_sensor.angle()
            correction = gyro_error * gyro_correct / current_speed
            self.left_wheel.run(current_speed - correction)
            self.right_wheel.run(current_speed + correction)
            print("Angle: ", self.left_wheel.angle(), " Speed: ", current_speed, "Error: ", gyro_error, " Correction: ", correction)
        self.stop()

    def turn_right(self, degrees, min_speed=MIN_RIGHT_TURN_SPEED, max_speed=MAX_RIGHT_TURN_SPEED, accel=DEFAULT_TURN_ACCELERATION, decel=DEFAULT_TURN_DECELERATION):
        start_angle = self.gyro_sensor.angle()
        stop_angle = start_angle + degrees - 1
        print("Turn Right: ", degrees, " Start at: ", start_angle, " Stop at: ", stop_angle)
        right_speed = min_speed
        while self.gyro_sensor.angle() < stop_angle:
            right_speed = self.calculate_speed(min_speed, max_speed, right_speed, start_angle, stop_angle, self.gyro_sensor.angle(), accel, decel)
            left_speed = right_speed * -1
            self.right_wheel.run(right_speed)
            self.left_wheel.run(left_speed)
            print("Angle: ", self.gyro_sensor.angle(), " Right Speed: ", right_speed)
        self.stop()

    def turn_left(self, degrees, min_speed=MIN_LEFT_TURN_SPEED, max_speed=MAX_LEFT_TURN_SPEED, accel=DEFAULT_TURN_ACCELERATION, decel=DEFAULT_TURN_DECELERATION):
        start_angle = self.gyro_sensor.angle()
        stop_angle = start_angle - degrees + 1
        print("Turn Left: ", degrees, " Start at: ", start_angle, " Stop at: ", stop_angle)
        right_speed = min_speed
        while self.gyro_sensor.angle() > stop_angle:
            right_speed = self.calculate_speed(min_speed, max_speed, right_speed, start_angle, stop_angle, self.gyro_sensor.angle(), accel, decel)
            left_speed = right_speed * -1
            self.right_wheel.run(right_speed)
            self.left_wheel.run(left_speed)
            print("Angle: ", self.gyro_sensor.angle(), " Right Speed: ", right_speed)
        self.stop()

    def turn_left_absolute(self, degrees, min_speed=MIN_LEFT_TURN_SPEED, max_speed=MAX_LEFT_TURN_SPEED, accel=DEFAULT_TURN_ACCELERATION, decel=DEFAULT_TURN_DECELERATION):
        right_speed = min_speed
        while self.gyro_sensor.angle() > degrees:
            self.right_wheel.run(min_speed)
            print("Angle: ", self.gyro_sensor.angle(), " Right Speed: ", right_speed)
        self.stop()
    
    def turn_left_pivot(self, degrees, min_speed=MIN_LEFT_TURN_SPEED, max_speed=MAX_LEFT_TURN_SPEED, accel=DEFAULT_TURN_ACCELERATION, decel=DEFAULT_TURN_DECELERATION):
        start_angle = self.gyro_sensor.angle()
        stop_angle = start_angle - degrees + 1
        print("Turn Left: ", degrees, " Start at: ", start_angle, " Stop at: ", stop_angle)
        right_speed = min_speed
        while self.gyro_sensor.angle() > stop_angle:
            right_speed = self.calculate_speed(min_speed, max_speed, right_speed, start_angle, stop_angle, self.gyro_sensor.angle(), accel, decel)
            self.right_wheel.run(right_speed)
            print("Angle: ", self.gyro_sensor.angle(), " Right Speed: ", right_speed)
        self.stop()

    def turn_left_pivot_back(self, degrees, min_speed=MIN_LEFT_TURN_SPEED, max_speed=MAX_LEFT_TURN_SPEED, accel=DEFAULT_TURN_ACCELERATION, decel=DEFAULT_TURN_DECELERATION):
        start_angle = self.gyro_sensor.angle()
        stop_angle = start_angle - degrees + 1
        print("Turn Left: ", degrees, " Start at: ", start_angle, " Stop at: ", stop_angle)
        right_speed = min_speed
        while self.gyro_sensor.angle() > stop_angle:
            right_speed = self.calculate_speed(min_speed, max_speed, right_speed, start_angle, stop_angle, self.gyro_sensor.angle(), accel, decel)
            self.left_wheel.run(-1 * right_speed)
            print("Angle: ", self.gyro_sensor.angle(), " Right Speed: ", right_speed)
        self.stop()

    def line_follow(self, inches, speed=LINE_FOLLOW_SPEED):
        degrees_to_move = inches * DEGREES_PER_INCH
        start_wheel_angle = self.left_wheel.angle()
        stop_wheel_angle = start_wheel_angle - degrees_to_move
        while self.left_wheel.angle() > stop_wheel_angle:
            right_reflection = self.color_sensor_right.reflection()
            left_reflection = self.color_sensor_left.reflection()
            diff = (right_reflection - left_reflection)
            correction = diff
            self.left_wheel.run(speed + correction)
            self.right_wheel.run(speed - correction)
        self.stop()

    def line_follow_to_divot(self, speed=LINE_FOLLOW_SPEED):
        biggest = 0
        self.gyro_sensor.reset_angle(0)
        while self.gyro_sensor.angle() < 15:
            right_reflection = self.color_sensor_right.reflection()
            left_reflection = self.color_sensor_left.reflection()
            diff = (right_reflection - left_reflection)
            correction = diff
            self.left_wheel.run(speed + correction)
            self.right_wheel.run(speed - correction)
            if (self.gyro_sensor.angle() > biggest):
                biggest = self.gyro_sensor.angle()
        brick.display.text(biggest)
        self.stop()

    def line_follow_to_black(self, speed=LINE_FOLLOW_SPEED):
        while self.color_sensor_left.reflection() > 15 or self.color_sensor_right.reflection() > 15:
            right_reflection = self.color_sensor_right.reflection()
            left_reflection = self.color_sensor_left.reflection()
            diff = (right_reflection - left_reflection)
            correction = diff / 2
            self.left_wheel.run(speed + correction)
            self.right_wheel.run(speed - correction)
        self.stop()
        
    def move_to_line(self, speed=150):
        self.left_wheel.run(speed)
        self.right_wheel.run(speed)
        while self.color_sensor_left.reflection() < 70:
            pass
        #while self.color_sensor_left.reflection() > 20:
            #pass
        self.stop()

    def square_to_black(self, speed = -100):
        stop_left = False
        stop_right = False
        while (not stop_left) or (not stop_right):
            right_reflection = self.color_sensor_right.reflection()
            left_reflection = self.color_sensor_left.reflection()
            diff = (right_reflection - left_reflection)
            correction = diff
            stop_left = stop_left or left_reflection < 20
            stop_right = stop_right or right_reflection < 20
            if (stop_left):
                self.left_wheel.stop(Stop.BRAKE)
            else:
                self.left_wheel.run(speed + correction)
            if (stop_right):
                self.right_wheel.stop(Stop.BRAKE)
            else:
                self.right_wheel.run(speed - correction)
        self.stop()

    def square_to_white(self, speed = 100):
        stop_left = False
        stop_right = False
        while (not stop_left) or (not stop_right):
            right_reflection = self.color_sensor_right.reflection()
            left_reflection = self.color_sensor_left.reflection()
            diff = (right_reflection - left_reflection)
            correction = diff
            stop_left = stop_left or left_reflection > 80
            stop_right = stop_right or right_reflection > 80
            if (stop_left):
                self.left_wheel.stop(Stop.BRAKE)
            else:
                self.left_wheel.run(speed + correction)
            if (stop_right):
                self.right_wheel.stop(Stop.BRAKE)
            else:
                self.right_wheel.run(speed - correction)
        self.stop()

    def left_motor_run_angle(self, speed, angle, brake = Stop.BRAKE):
        self.motor_run_angle(self.left_motor, speed, angle, brake)

    def right_motor_run_angle(self, speed, angle, brake = Stop.BRAKE):
        self.motor_run_angle(self.right_motor, speed, angle, brake)

    def motor_run_angle(self, motor, speed, angle, brake):
        target = motor.angle()
        if speed < 0:
            target = target - angle
            while motor.angle() > target:
                motor.run(speed)
        else:
            target = target + angle
            while motor.angle() < target:
                motor.run(speed)
        motor.stop(brake)
