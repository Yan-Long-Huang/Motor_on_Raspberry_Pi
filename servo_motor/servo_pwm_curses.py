#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
import time
import Adafruit_PCA9685
import sys,os
import curses

def draw_menu(stdscr):
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
            return pulse

    channel = 0
    servo = Servo(channel,100,640) # YF-6125MG 180° servo motor.
    angle = 0


    k = 0
    cursor_x = 0
    cursor_y = 0

    # Clear and refresh the screen for a blank canvas
    stdscr.clear()
    stdscr.refresh()

    # Start colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)

    # Loop where k is the last character pressed
    while (k != ord('q')):

        # Initialization
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        if k == curses.KEY_UP:
            angle = 180
        elif k == curses.KEY_DOWN or k == ord(' ') or k == ord('Z') or k == ord('z') or k == ord('K') or k == ord('k'):
            angle = 0
        elif k == curses.KEY_LEFT:
            angle -= 1
        elif k == curses.KEY_RIGHT:
            angle += 1
        elif k == ord('J') or k == ord('j'):
            angle -= 5
        elif k == ord('L') or k == ord('l'):
            angle += 5
        elif k == ord('X') or k == ord('x'):
            angle = 70
        if angle < 0:angle=0
        if angle > 180:angle=180

        pulse = servo.set_angle(angle)


        cursor_x = max(0, cursor_x)
        cursor_x = min(width-1, cursor_x)

        cursor_y = max(0, cursor_y)
        cursor_y = min(height-1, cursor_y)

        # Declaration of strings
        title = "PCA9685 Servo Test"[:width-1]
        subtitle = "Press ↑,↓,←,→,X,Z and Space to Control Servo Motor."[:width-1]
        keystr = "angle= {} (pulse:{})".format(angle,pulse)[:width-1]
        statusbarstr = "Press 'q' to exit | Console Window [{}×{}]".format(width, height)
        if k == 0:
            keystr = "No key press detected..."[:width-1]

        # Centering calculations
        start_x_title = int((width // 2) - (len(title) // 2) - len(title) % 2)
        start_x_subtitle = int((width // 2) - (len(subtitle) // 2) - len(subtitle) % 2)
        start_x_keystr = int((width // 2) - (len(keystr) // 2) - len(keystr) % 2)
        start_y = int((height // 2) - 2)

        # Rendering some text
        whstr = ""
        stdscr.addstr(0, 0, whstr, curses.color_pair(1))

        # Render status bar
        stdscr.attron(curses.color_pair(3))
        stdscr.addstr(height-1, 0, statusbarstr)
        stdscr.addstr(height-1, len(statusbarstr), " " * (width - len(statusbarstr) - 1))
        stdscr.attroff(curses.color_pair(3))

        # Turning on attributes for title
        stdscr.attron(curses.color_pair(2))
        stdscr.attron(curses.A_BOLD)

        # Rendering title
        stdscr.addstr(start_y, start_x_title, title)

        # Turning off attributes for title
        stdscr.attroff(curses.color_pair(2))
        stdscr.attroff(curses.A_BOLD)

        # Print rest of text
        stdscr.addstr(start_y + 1, start_x_subtitle, subtitle)
        stdscr.addstr(start_y + 3, (width // 2) - 2, '-' * 4)
        stdscr.addstr(start_y + 5, start_x_keystr, keystr)
        stdscr.move(cursor_y, cursor_x)

        # Refresh the screen
        stdscr.refresh()

        # Wait for next input
        k = stdscr.getch()

def main():
    curses.wrapper(draw_menu)

if __name__ == "__main__":
    main()
