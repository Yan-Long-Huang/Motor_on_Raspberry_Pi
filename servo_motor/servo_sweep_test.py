from __future__ import division
import time
import Adafruit_PCA9685
import sys,os

""" Servo Motor """
class Servo:
    def __init__(self,channel,pulse_min=150,pulse_max=600,angle_min=0,angle_max=180,reverse=False,freq=60):
        self.__pwm = Adafruit_PCA9685.PCA9685()
        self.__pwm.set_pwm_freq(freq)
        self.__channel = channel
        self.__pulse_min = pulse_min
        self.__pulse_max = pulse_max
        if reverse == False:
            self.__angle_min = angle_min
            self.__angle_max = angle_max
        else:
            self.__angle_min = angle_max
            self.__angle_max = angle_min

        self.__pulse = 0

    def set_angle(self,angle = 'no-change'): # set_angle(none) -> current pulse
        if angle != 'no-change':
            if angle < self.__angle_min: angle = self.__angle_min
            elif angle > self.__angle_max: angle = self.__angle_max
            self.__pulse = int((angle - self.__angle_min) * (self.__pulse_max - self.__pulse_min) / (self.__angle_max - self.__angle_min) + self.__pulse_min)
            self.__pwm.set_pwm(self.__channel, 0, self.__pulse)
        return self.__pulse

    def set_pulse(self, pulse = 'no-change'): # set_pulse(none) -> current angle
        if pulse != 'no-change':
            self.__pulse = int(pulse)
            self.__pwm.set_pwm(self.__channel, 0, self.__pulse)
        return (self.__pulse - self.__pulse_min) * (self.__angle_max - self.__angle_min) / (self.__pulse_max - self.__pulse_min) + self.__angle_min

    def pwm_off(self):
        self.__pwm.set_pwm(self.__channel, 0, 0)

    def lesion(self): # KILL SERVO
        self.set_angle(0)
        time.sleep(2)
        self.set_angle(150)
        time.sleep(2)
        self.set_angle(0)
        time.sleep(0.5)
        self.pwm_off()

""" main """
# define servo motor
channel=0
pulse_min=146
pulse_max=666
angle_min=0
angle_max=180
reverse=False

servo=Servo(channel,pulse_min,pulse_max,angle_min,angle_max,reverse)

try:
    # Loop to control the servo motor repeatedly
    while True:
        servo.set_angle(0) # turn to 0 degree
        time.sleep(1) # wait for 1 second
        servo.set_angle(90) # turn to 90 degree
        time.sleep(1) # wait for 1 second
        servo.set_angle(180) # turn to 180 degree
        time.sleep(1) # wait for 1 second
        servo.set_angle(90) # turn back to 90 degree
        time.sleep(1) # wait for 1 second

except KeyboardInterrupt:
    pass

finally:
    print("Final processing...")
    # servo.set_angle(90)
    # time.sleep(1)
    servo.pwm_off()
    print("Finish.")
