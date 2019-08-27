#!/usr/bin/env pybricks-micropython

from pybricks import ev3brick as brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color,
                                 SoundFile, ImageFile, Align)
from pybricks.tools import print, wait, StopWatch
from pybricks.robotics import DriveBase

def watchDistance():
    sensor = UltrasonicSensor(Port.S1)
    while True: 
        distance = sensor.distance()
        print (distance)
        if distance > 1600:
            brick.light(Color.GREEN)
        if distance < 1600:
            brick.sound.beep(1400 - distance, 100, 20)
        if distance < 1200:
            brick.light(Color.YELLOW)
        if distance < 800:
            brick.light(Color.ORANGE)
        if distance < 400:
            brick.light(Color.RED)
        
            