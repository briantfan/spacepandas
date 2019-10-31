#!/usr/bin/env pybricks-micropython

from pybricks import ev3brick as brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color,
                                 SoundFile, ImageFile, Align)
from pybricks.tools import print, wait, StopWatch
from pybricks.robotics import DriveBase

def watchDistance():
    # Setup the ultrasonic sensor on Port 1
    sensor = UltrasonicSensor(Port.S1)
    while True: 
        distance = sensor.distance()
        print(distance)
        if distance > 1600:
            # Show a green light for objects more than 1.6m away.
            brick.light(Color.GREEN)
        if distance < 1600:
            # Beep for objects less than 1.6m away.
            # Closer objects will get a higher pitch.
            brick.sound.beep(1400 - distance, 100, 20)
        if distance < 1200:
            # Show a yellow light for objects less than 1.2m away.
            brick.light(Color.YELLOW)
        if distance < 800:
            # Show an orange light for objects less than 0.8m away.
            brick.light(Color.ORANGE)
        if distance < 400:
            # Show a red light for objects less than 0.4m away.
            brick.light(Color.RED)
