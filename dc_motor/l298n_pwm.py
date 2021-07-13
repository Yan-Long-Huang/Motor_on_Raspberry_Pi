#!/usr/bin/env python3
#coding=utf-8
import Adafruit_PCA9685
import RPi.GPIO as GPIO
import getch
import time

""" PCA9685 """ 
class PCA9685_PWM: # A channel of PCA9685
    def __init__(self, channel, min=-4095, max=4095, freq=60):
        self.__pwm = Adafruit_PCA9685.PCA9685()
        self.__pwm.set_pwm_freq(freq) # adjust the PWM frequency,
        self.__channel = channel # A PCA9685 PWM channel (0~15)
        self.__min = min # Pulse minimum limit
        self.__max = max # Pulse maximum limit

    def __limit(self, pulse):
        if pulse >= self.__min and pulse <= self.__max:
            return pulse
        elif pulse < self.__min:
            return self.__min
        elif pulse > self.__max:
            return self.__max

    def set_pwm(self, pulse):
        pulse = self.__limit(pulse)
        self.__pwm.set_pwm(self.__channel, 0, pulse)
        return pulse
    def pwm_off(self):
        self.__pwm.set_pwm(self.__channel, 0, 0)
    

""" DC Motor """
GPIO.setmode(GPIO.BCM)
# GPIO.setwarnings(False) 

class L298N_DC_Motor: # Class for L298N DC motor driver
    def __init__(self, pca9685, input): # Parameter is used to set the PCA9685 and GPIO channels
        self.__pca9685 = PCA9685_PWM(pca9685) # Create a object of PCA9685_PWM class for EN
        self.__gpio = input
        # print(f"gpio[0]= {input[0]}, gpio[1]= {input[1]}")
        self.__rotate_val = 0
        GPIO.setup(self.__gpio[0], GPIO.OUT)
        GPIO.setup(self.__gpio[1], GPIO.OUT)
        self.__stop()

    def __stop(self):
        GPIO.output(self.__gpio[0], GPIO.LOW)
        GPIO.output(self.__gpio[1], GPIO.LOW)
        self.__pca9685.pwm_off()
    def __forward(self):
        GPIO.output(self.__gpio[0], GPIO.HIGH)
        GPIO.output(self.__gpio[1], GPIO.LOW)
        print("forward")
    def __backward(self):
        GPIO.output(self.__gpio[0], GPIO.LOW)
        GPIO.output(self.__gpio[1], GPIO.HIGH)
        print("backward")
    def __set_speed(self, pulse):
        self.__pca9685.set_pwm(pulse)

    def rotate(self, rotate_val):
        if rotate_val == 0:
            self.__stop()
        elif rotate_val > 0:
            self.__forward()
            self.__set_speed(abs(rotate_val))
        elif rotate_val < 0:
            self.__backward()
            self.__set_speed(abs(rotate_val))
        self.__rotate_val = rotate_val


""" Define """
motor=L298N_DC_Motor(0,[17,18])

KEY_UP = 65
KEY_DOWN = 66
KEY_LEFT = 68
KEY_RIGHT = 67

def limit(pulse, min, max ):
    if pulse >= min and pulse <= max:
        return pulse
    elif pulse < min:
        return min
    elif pulse > max:
        return max

""" main """

rotate_val = 0

try:
    while True: 
        rotate_val=limit(rotate_val,-4095,4095)
        motor.rotate(rotate_val)
        print(f"rotate_val= {rotate_val}")

        keycode = ord(getch.getch()) 
        if keycode == 27  and ord(getch.getch()) == 91:
            keycode = ord(getch.getch())
            if keycode == KEY_UP:
                rotate_val+=1
            elif keycode == KEY_DOWN:
                rotate_val-=1
            elif keycode == KEY_LEFT:
                rotate_val-=50
            elif keycode == KEY_RIGHT:
                rotate_val+=50
        elif keycode == ord(' '):
            rotate_val = 0

except KeyboardInterrupt:
    rotate_val = 0

finally:
    print("<Finish>")
    motor.rotate(0)
    GPIO.cleanup()
