#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
import time
import Adafruit_PCA9685

class Servo:
    def __init__(self,channel,min=150,max=600,freq=60):
        self.pwm = Adafruit_PCA9685.PCA9685()
        self.pwm.set_pwm_freq(freq)
        self.channel = channel
        self.min=min
        self.max=max
    
    def set_angle(self,angle):
        pulse = int((angle - 0) * (self.max - self.min) / (180 - 0) + self.min)
        self.pwm.set_pwm(self.channel, 0, pulse)

""" main """
channel = 0
servo_1 = Servo(channel,100,646) # YF-6125MG 180° servo motor.
print(f"\nprint('Moving servo on channel {channel}, press Ctrl-C to quit...')")

try:
    while True:
        servo_1.set_angle(int(input("angle= ")))
except KeyboardInterrupt:
    print ("\n\n<Ctrl-C>") 
except:
    print ("Other error or exception occurred!")
finally:
    print ("\n-- Finish --\n")
