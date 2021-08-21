#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
import time
import Adafruit_PCA9685
import sys,os
import curses
import getch

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


""" Consol Window """
stdscr = curses.initscr()

# Clear and refresh the screen for a blank canvas
stdscr.clear()
stdscr.refresh()

# Start colors in curses
curses.start_color()
curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_RED)
curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)

# Text View
class TextView:
    def __init__(self,x_offset=0,y_offset=0,text=""):
        self.__x_offset=x_offset
        self.__y_offset=y_offset
        self.__text=text
    
    def print_txv(self,message=""): # Make a function to print a line in the center of screen
        # stdscr.refresh()
        if message!= "":
            self.__text = message

        num_rows, num_cols = stdscr.getmaxyx()

        x_position = int(num_cols / 2) - int(len(self.__text) / 2) + self.__x_offset # middle_column - half_length_of_message
        if x_position < 0: x_position = 0
        elif x_position > num_cols: x_position = num_cols - int(len(self.__text))-1

        y_position = int(num_rows / 2) - self.__y_offset # middle_row + self.__y_offset
        if y_position < 0: y_position = 0
        elif y_position > num_rows: y_position = num_rows-1

        # Draw the text
        stdscr.addstr(y_position, x_position, self.__text)
        stdscr.move(num_rows-1, num_cols-1) # stdscr.move(0, 0)

def print_tittle():
    tittle=TextView(0,3," PCA9685 One Servo Test ")
    separator=TextView(0,2,"Press ↑,↓,←,→,W,A,S,D and Space to Control Servo Motor.")
    stdscr.attron(curses.color_pair(2))
    tittle.print_txv()
    stdscr.attroff(curses.color_pair(2))
    separator.print_txv()

def print_servo_status():
    x_offset = 0
    stdscr.attron(curses.color_pair(1))
    servo_txv=TextView(x_offset,0,"channel:{:>2}".format(channel))
    servo_txv.print_txv()
    stdscr.attroff(curses.color_pair(1))
    angle_txv=TextView(x_offset,-1,"angle= {:>3}".format(servo.set_pulse()))
    angle_txv.print_txv()
    pulse_txv=TextView(x_offset,-2,"pulse= {:>3}".format(servo.set_angle()))
    pulse_txv.print_txv()

def print_satatus_bar():
    statusbar=TextView(-9999,-9999)
    num_rows, num_cols = stdscr.getmaxyx()
    stdscr.attron(curses.color_pair(3))
    str = "Press 'q' or Tab to exit | Console Window [{}×{}]".format(num_cols, num_rows)
    statusbar.print_txv(str+ " " * (num_cols - len(str) - 1))
    stdscr.attroff(curses.color_pair(3))

def print_all():
    stdscr.clear()
    print_tittle()

    print_servo_status()

    print_satatus_bar()
    stdscr.refresh()



""" main """
# define Servo0
channel=0
pulse_min=146
pulse_max=666
angle_min=0
angle_max=180
reverse=False

servo=Servo(channel,pulse_min,pulse_max,angle_min,angle_max,reverse)

KEY_UP = 65
KEY_DOWN = 66
KEY_LEFT = 68
KEY_RIGHT = 67
max_key={ord('W'):0,ord('w'):0}
inc_key={ord('D'):0,ord('d'):0}
dec_key={ord('A'):0,ord('a'):0}
min_key={ord('S'):0,ord('s'):0}
func_key={ord(' '):0}

def limit(pulse, min, max ):
    if pulse >= min and pulse <= max:
        return pulse
    elif pulse < min:
        return min
    elif pulse > max:
        return max

try:
    keycode=0
    servo_pulse=(pulse_min + pulse_max)/2
    
    # Loop where k is the last character pressed
    while (keycode != ord('q') and keycode!= ord('\t')):
        servo_pulse = limit(servo_pulse,pulse_min,pulse_max)
        servo.set_pulse(servo_pulse)
        print_all()

        keycode = ord(getch.getch()) 
        if keycode == 27  and ord(getch.getch()) == 91:
            keycode = ord(getch.getch())
            if keycode == KEY_UP:
                servo_pulse+=10
            elif keycode == KEY_DOWN:
                servo_pulse-=10
            elif keycode == KEY_LEFT:
                servo_pulse-=1
            elif keycode == KEY_RIGHT:
                servo_pulse+=1
        elif max_key.get(keycode)!=None:
            servo_pulse+=10
        elif inc_key.get(keycode)!=None:
            servo_pulse+=1
        elif dec_key.get(keycode)!=None:
            servo_pulse-=1
        elif min_key.get(keycode)!=None:
            servo_pulse-=10
        elif func_key.get(keycode)!=None:
            servo_pulse=(pulse_min + pulse_max)/2

except KeyboardInterrupt:
    pass

finally:
    curses.endwin()
    print("Final processing...")
    servo.set_angle(90)
    time.sleep(1)
    servo.pwm_off()
    print("Finish.")
