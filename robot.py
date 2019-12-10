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
MAX_FORWARD_SPEED = -800
MIN_BACKWARD_SPEED = 60
MAX_BACKWARD_SPEED = 800

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

    # Initialize and setup the robot and all motors and sensors.
    def __init__(self):
        self.right_wheel = Motor(Port.B)
        self.left_wheel = Motor(Port.C)
        self.left_motor = Motor(Port.D)
        self.right_motor = Motor(Port.A)
        self.color_sensor_right = ColorSensor(Port.S2)
        self.color_sensor_left = ColorSensor(Port.S3)
        self.gyro_sensor = GyroSensor(Port.S4, Direction.CLOCKWISE)
        self.left_motor.set_pid_settings(100, 50, 1, 1000, 50, 50, 0, 1000)
        self.right_motor.set_pid_settings(100, 50, 1, 1000, 50, 50, 0, 1000)
        self.stopwatch = StopWatch()
        self.check_gyro()

    # Diagnostic test that will beep if the gyro is not calibrated.
    def check_gyro(self):
        brick.sound.beep()
        gyro_angle = self.gyro_sensor.angle()
        wait(2000)  # wait 2 seconds
        if gyro_angle != self.gyro_sensor.angle():
            # Make a lower-sounding beep to let us know something is wrong.
            brick.sound.beep(400, 500, 30)
        else:
            brick.sound.beep()

    # Stop and brake the wheels.
    def stop(self):
        self.right_wheel.run(0)
        self.left_wheel.run(0)
        self.right_wheel.stop(Stop.BRAKE)
        self.left_wheel.stop(Stop.BRAKE)
    
    # Range check a value
    def range_check(self, value, min, max):
        if value < min:
            return min
        if value > max:
            return max
        return value

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
    
    # Figure out how fast we should go based on our current position.
    def calculate_speed(self, min_speed, max_speed, current_speed, start_angle, stop_angle, current_angle, accel, decel):
        # Figure out when we should start slowing down.
        decel_angle = stop_angle - ((current_speed - min_speed) / (decel / accel))
        # We shouldn't accelerate past the mid-way point or decelerate before that.
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

    # Move forward, since the motors are upside-down, speed is negative.
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
            correction = self.range_check(gyro_error * gyro_correct / current_speed, -100, 100)
            self.left_wheel.run(current_speed + correction)
            self.right_wheel.run(current_speed - correction)
            print("Angle: ", self.left_wheel.angle(), " Speed: ", current_speed, "Error: ", gyro_error, " Correction: ", correction)
        self.stop()

    # Move forward, since the motors are upside-down, speed is negative. Watch both wheels.
    def forward2(self, inches, millis, min_speed=MIN_FORWARD_SPEED, max_speed=MAX_FORWARD_SPEED, accel=DEFAULT_MOVE_ACCELERATION, decel=DEFAULT_MOVE_DECELERATION, gyro_correct=GYRO_CORRECTION):
        degrees_to_move = inches * DEGREES_PER_INCH
        left_start_angle = self.left_wheel.angle()
        right_start_angle = self.right_wheel.angle()
        left_stop_angle = left_start_angle - degrees_to_move
        right_stop_angle = right_start_angle - degrees_to_move
        print("Inches in Degrees: ", degrees_to_move, "Start: ", left_start_angle, " Stop: ", left_stop_angle)
        start_gyro_angle = self.gyro_sensor.angle()
        current_speed = min_speed
        self.stopwatch.reset()
        while self.left_wheel.angle() > left_stop_angle and self.right_wheel.angle() > right_stop_angle and self.stopwatch.time() < millis:
            current_speed = self.calculate_speed(min_speed, max_speed, current_speed, left_start_angle, left_stop_angle, self.left_wheel.angle(), accel, decel)
            gyro_error = start_gyro_angle - self.gyro_sensor.angle()
            correction = self.range_check(gyro_error * gyro_correct / current_speed, -100, 100)
            self.left_wheel.run(current_speed + correction)
            self.right_wheel.run(current_speed - correction)
            print("Angle: ", self.left_wheel.angle(), " Speed: ", current_speed, "Error: ", gyro_error, " Correction: ", correction)
        self.stop()

    # Move backward, since the motors are upside-down, speed is positive.
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
            correction = self.range_check(gyro_error * gyro_correct / current_speed, -100, 100)
            self.left_wheel.run(current_speed - correction)
            self.right_wheel.run(current_speed + correction)
            print("Angle: ", self.left_wheel.angle(), " Speed: ", current_speed, "Error: ", gyro_error, " Correction: ", correction)
        self.stop()

    # Move backward, since the motors are upside-down, speed is positive.
    def backward2(self, inches, min_speed=MIN_BACKWARD_SPEED, max_speed=MAX_BACKWARD_SPEED, accel=DEFAULT_MOVE_ACCELERATION, decel=DEFAULT_MOVE_DECELERATION, gyro_correct=GYRO_CORRECTION):
        degrees_to_move = inches * DEGREES_PER_INCH
        left_start_angle = self.left_wheel.angle()
        right_start_angle = self.right_wheel.angle()
        left_stop_angle = left_start_angle + degrees_to_move
        right_stop_angle = right_start_angle + degrees_to_move
        print("Inches in Degrees: ", degrees_to_move, "Start: ", left_start_angle, " Stop: ", left_stop_angle)
        start_gyro_angle = self.gyro_sensor.angle()
        current_speed = min_speed
        while self.left_wheel.angle() < left_stop_angle and self.right_wheel.angle() < right_stop_angle:
            current_speed = self.calculate_speed(min_speed, max_speed, current_speed, left_start_angle, left_stop_angle, self.left_wheel.angle(), accel, decel)
            gyro_error = start_gyro_angle - self.gyro_sensor.angle()
            correction = self.range_check(gyro_error * gyro_correct / current_speed, -100, 100)
            self.left_wheel.run(current_speed - correction)
            self.right_wheel.run(current_speed + correction)
            print("Angle: ", self.left_wheel.angle(), " Speed: ", current_speed, "Error: ", gyro_error, " Correction: ", correction)
        self.stop()

    # Move backward, since the motors are upside-down, speed is positive.
    def backward_or_wait(self, inches, millis, min_speed=MIN_BACKWARD_SPEED, max_speed=MAX_BACKWARD_SPEED, accel=DEFAULT_MOVE_ACCELERATION, decel=DEFAULT_MOVE_DECELERATION, gyro_correct=GYRO_CORRECTION):
        degrees_to_move = inches * DEGREES_PER_INCH
        start_angle = self.left_wheel.angle()
        stop_angle = start_angle + degrees_to_move
        print("Inches in Degrees: ", degrees_to_move, "Start: ", start_angle, " Stop: ", stop_angle)
        start_gyro_angle = self.gyro_sensor.angle()
        current_speed = min_speed
        self.stopwatch.reset()
        while self.left_wheel.angle() < stop_angle and self.stopwatch.time() < millis:
            current_speed = self.calculate_speed(min_speed, max_speed, current_speed, start_angle, stop_angle, self.left_wheel.angle(), accel, decel)
            gyro_error = start_gyro_angle - self.gyro_sensor.angle()
            correction = self.range_check(gyro_error * gyro_correct / current_speed, -100, 100)
            self.left_wheel.run(current_speed - correction)
            self.right_wheel.run(current_speed + correction)
            print("Angle: ", self.left_wheel.angle(), " Speed: ", current_speed, "Error: ", gyro_error, " Correction: ", correction)
        self.stop()

    # Turn right, use the gyro sensor to tell when to stop.
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

    # Turn left, use the gyro sensor to tell when to stop.
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

    # Turn left based on our absolute heading.
    # The gyro sensor must be calibrated and reset for this to work.
    def turn_left_absolute(self, degrees, min_speed=MIN_LEFT_TURN_SPEED, max_speed=MAX_LEFT_TURN_SPEED, accel=DEFAULT_TURN_ACCELERATION, decel=DEFAULT_TURN_DECELERATION):
        right_speed = min_speed
        while self.gyro_sensor.angle() > degrees:
            self.right_wheel.run(min_speed)
            print("Angle: ", self.gyro_sensor.angle(), " Right Speed: ", right_speed)
        self.stop()
    
    # Turn left based on our absolute heading.
    # The gyro sensor must be calibrated and reset for this to work.
    def turn_left_absolute2(self, degrees, min_speed=MIN_LEFT_TURN_SPEED, max_speed=MAX_LEFT_TURN_SPEED, accel=DEFAULT_TURN_ACCELERATION, decel=DEFAULT_TURN_DECELERATION):
        print("Turn left absolute 2:  start: ", self.gyro_sensor.angle(), "  target: ", degrees)
        while self.gyro_sensor.angle() > degrees:
            self.left_wheel.run(min_speed)
            print("Angle: ", self.gyro_sensor.angle(), " Left Speed: ", min_speed)
        self.stop()
    
    # Turn left by pivoting on the left wheel and moving the right wheel forward.
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

    # Turn left by pivoting on the right wheel and moving the left wheel backward.
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

    # Turn right pivot use the gyro sensor to tell when to stop.
    def turn_right_pivot(self, degrees, min_speed=MIN_RIGHT_TURN_SPEED, max_speed=MAX_RIGHT_TURN_SPEED, accel=DEFAULT_TURN_ACCELERATION, decel=DEFAULT_TURN_DECELERATION):
        start_angle = self.gyro_sensor.angle()
        stop_angle = start_angle + degrees - 1
        print("Turn Right: ", degrees, " Start at: ", start_angle, " Stop at: ", stop_angle)
        right_speed = min_speed
        while self.gyro_sensor.angle() < stop_angle:
            right_speed = self.calculate_speed(min_speed, max_speed, right_speed, start_angle, stop_angle, self.gyro_sensor.angle(), accel, decel)
            left_speed = right_speed * -1
            self.left_wheel.run(left_speed)
            print("Angle: ", self.gyro_sensor.angle(), " Right Speed: ", right_speed)
        self.stop()

    # Line follow for a certain distance. This can be inaccurate because of line following adjustments.
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

    # Line follow for a certain distance. This can be inaccurate because of line following adjustments.
    def line_follow2(self, inches, speed=LINE_FOLLOW_SPEED):
        degrees_to_move = inches * DEGREES_PER_INCH
        left_start_wheel_angle = self.left_wheel.angle()
        right_start_wheel_angle = self.right_wheel.angle()
        left_stop_wheel_angle = left_start_wheel_angle - degrees_to_move
        right_stop_wheel_angle = right_start_wheel_angle - degrees_to_move
        while self.left_wheel.angle() > left_stop_wheel_angle and self.right_wheel.angle() > right_stop_wheel_angle:
            right_reflection = self.color_sensor_right.reflection()
            left_reflection = self.color_sensor_left.reflection()
            diff = (right_reflection - left_reflection)
            correction = diff
            self.left_wheel.run(speed + correction)
            self.right_wheel.run(speed - correction)
        self.stop()

    #Line follow until we reach the first divot in the longest line.
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

    # Line follow until we hit the black line at the bottom of the ramp.
    def line_follow_to_black(self, speed=LINE_FOLLOW_SPEED):
        while self.color_sensor_left.reflection() > 15 or self.color_sensor_right.reflection() > 15:
            right_reflection = self.color_sensor_right.reflection()
            left_reflection = self.color_sensor_left.reflection()
            diff = (right_reflection - left_reflection)
            correction = diff / 2
            self.left_wheel.run(speed + correction)
            self.right_wheel.run(speed - correction)
        self.stop()
        
    # Line follow for a certain distance. This can be inaccurate because of line following adjustments.
    def line_follow_to_end(self, inches, speed=LINE_FOLLOW_SPEED):
        degrees_to_move = inches * DEGREES_PER_INCH
        start_wheel_angle = self.left_wheel.angle()
        stop_wheel_angle = start_wheel_angle - degrees_to_move
        while self.left_wheel.angle() > stop_wheel_angle and self.color_sensor_left.reflection() < 80 and self.color_sensor_right.reflection() < 80:
            if self.color_sensor_left.reflection() < 25 and self.color_sensor_right.reflection() < 25:
                break
            right_reflection = self.color_sensor_right.reflection()
            left_reflection = self.color_sensor_left.reflection()
            diff = (right_reflection - left_reflection)
            correction = diff
            self.left_wheel.run(speed + correction)
            self.right_wheel.run(speed - correction)
        self.stop()

    # Move forward until we see a white line. No gyro corrections are made.
    def move_to_line(self, inches, speed=-150):
        degrees_to_move = inches * DEGREES_PER_INCH
        start_wheel_angle = self.left_wheel.angle()
        stop_wheel_angle = start_wheel_angle - degrees_to_move
        self.left_wheel.run(speed)
        self.right_wheel.run(speed)
        while self.color_sensor_right.reflection() < 70 and self.left_wheel.angle() > stop_wheel_angle:
            pass
        #brick.sound.beep()
        while self.color_sensor_right.reflection() > 20 and self.left_wheel.angle() > stop_wheel_angle:
            pass
        #brick.sound.beep()
        while self.color_sensor_right.reflection() < 70 and self.left_wheel.angle() > stop_wheel_angle:
            pass
        #brick.sound.beep()
        self.stop()
        
    # Move forward until we see a white line. No gyro corrections are made.
    def move_to_line_backwards(self, speed=150):
        self.left_wheel.run(speed)
        self.right_wheel.run(speed)
        while self.color_sensor_left.reflection() < 70:
            pass
        self.stop()

    def drive_right(self, degrees, left_speed, right_speed):
        start_angle = self.gyro_sensor.angle()
        stop_angle = start_angle + degrees - 1
        while self.gyro_sensor.angle() < stop_angle:
            self.right_wheel.run(right_speed)
            self.left_wheel.run(left_speed)

    def drive_left(self, degrees, left_speed, right_speed):
        start_angle = self.gyro_sensor.angle()
        stop_angle = start_angle - degrees + 1
        while self.gyro_sensor.angle() > stop_angle:
            self.right_wheel.run(right_speed)
            self.left_wheel.run(left_speed)
