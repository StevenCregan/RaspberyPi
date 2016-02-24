#!/usr/bin/python
# 
# Creator     : Steven Cregan
# Date        : 02/21/16
# Description : This program will move a small vehicle forwards,
#               backwards, left, and right as controlled by 
#               an Xbox360 wireless controller
import RPi.GPIO as GPIO
import time
import os
import sys
import re
import threading
# Credit to Zephod on github
# https://github.com/zephod/lego-pi
sys.path.insert(0, '/home/pi/')
from legopi.lib import xbox_read

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
# Set the pin positions of buttons
lbutton = 26
rbutton = 19
# Set the buttons as Pull-UP current, and input
GPIO.setup(lbutton, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(rbutton, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# Set the pin positions of the LED's
lled = 6
rled = 13
# Set LED's as output
GPIO.setup(lled, GPIO.OUT)
GPIO.setup(rled, GPIO.OUT)

# Since we're using stepper motors, declare max switching speed
motorspeed = 10
delay = motorspeed/10000.0

# Right Side Motors
# Just some wire colors for personal clarity
# blue
rightMotorPin1 = 18
# white
rightMotorPin2 = 23
# yellow
rightMotorPin3 = 24
# orange
rightMotorPin4 = 25

# Set the motor pins as output
GPIO.setup(rightMotorPin1, GPIO.OUT)
GPIO.setup(rightMotorPin2, GPIO.OUT)
GPIO.setup(rightMotorPin3, GPIO.OUT)
GPIO.setup(rightMotorPin4, GPIO.OUT)

# Left Side Motors
# Just some wire colors for personal clarity
# blue
leftMotorPin1 =  4
# white
leftMotorPin2 = 17
# yellow
leftMotorPin3 = 27
# orange
leftMotorPin4 = 22

# Set the motor pins as output
GPIO.setup(leftMotorPin1, GPIO.OUT)
GPIO.setup(leftMotorPin2, GPIO.OUT)
GPIO.setup(leftMotorPin3, GPIO.OUT)
GPIO.setup(leftMotorPin4, GPIO.OUT)

# Declare and define "backwards" motion
def backward(arg1, stop_event):
    while(not stop_event.is_set()):
        time.sleep(delay)
        setStep(1,0,0,0)
        time.sleep(delay)
        setStep(1,0,0,1)
        time.sleep(delay)
        setStep(0,0,0,1)
        time.sleep(delay)
        setStep(0,0,1,1)
        time.sleep(delay)
        setStep(0,0,1,0)
        time.sleep(delay)
        setStep(0,1,1,0)
        time.sleep(delay)
        setStep(0,1,0,0)
        time.sleep(delay)
        setStep(1,1,0,0)
        time.sleep(delay)

# Declare and define "forwards" motion
def forward(arg1, stop_event):
    while(not stop_event.is_set()):
        time.sleep(delay)
        setStep(1,0,0,0)
        time.sleep(delay)
        setStep(1,1,0,0)
        time.sleep(delay)
        setStep(0,1,0,0)
        time.sleep(delay)
        setStep(0,1,1,0)
        time.sleep(delay)
        setStep(0,0,1,0)
        time.sleep(delay)
        setStep(0,0,1,1)
        time.sleep(delay)
        setStep(0,0,0,1)
        time.sleep(delay)
        setStep(1,0,0,1)
        time.sleep(delay)

# The setStep function actually sets the voltage on the pins.
# since it's being used for STEPPER motors, take 4 args (1 or 0)
def setStep(w1, w2, w3, w4):

    GPIO.output( rightMotorPin1, w1)
    GPIO.output( leftMotorPin1,  w4)

    GPIO.output( rightMotorPin2, w2)
    GPIO.output( leftMotorPin2,  w3)

    GPIO.output( rightMotorPin3, w3)
    GPIO.output( leftMotorPin3,  w2)

    GPIO.output( rightMotorPin4, w4)
    GPIO.output( leftMotorPin4,  w1)

# This function is here as a guarantee the motors will be
# released properly, with all pins set low
def off():
    setStep(0,0,0,0)
    time.sleep(delay)

def main():
    # Store controller values
    A = 0
    B = 0
    Y1 = 0
    X1 = 0
    # Declare our threads
    # Don't forget, set the threads as daemon to keep them from persisting
    tForward_stop = threading.Event()
    tForward = threading.Thread(target = forward, args=(1, tForward_stop))
    tForward.daemon = True

    tBackward_stop = threading.Event()
    tBackward = threading.Thread(target = backward, args=(2, tBackward_stop))
    tBackward.daemon = True

    while True:
        for event in xbox_read.event_stream(deadzone=12000):
#            print str(event)
            input_state_L = GPIO.input(lbutton)
            input_state_R = GPIO.input(rbutton)
    
            if  ((event.key == "A") and (event.value == 1)):
                A = 1
                pass
            elif((event.key == "A") and (event.value == 0)):
                A = 0
                pass
            elif((event.key == "B") and (event.value == 1)):
                B = 1
                pass
            elif((event.key == "B") and (event.value == 0)):
                B = 0
                pass
            elif((event.key == "Y1")):
                Y1 = event.value
                pass
            else:
                pass

            if   (A  == 0):
                input_state_L = 1
                pass
            elif (A  == 1):
                input_state_L = 0
                pass

            if   (B  == 0):
                input_state_R = 1
                pass
            elif (B  == 1):
                input_state_R = 0
                pass

            if   (A == 0) and (B == 0):
                if (Y1 == 0):
                    input_state_L = 1
                    input_state_R = 1
                    pass
                elif (Y1  > 0):
                    input_state_L = 0
                    pass
                elif (Y1  < 0):
                    input_state_R = 0
                    pass

            if   (X1 == 0):
                pass
            elif (X1  > 0):
                pass
            elif (X1  < 0):
                pass

#            print ("A = {0} , B = {1}").format(A, B)
#            print ("{0}  ,  {1}").format(input_state_L, input_state_R)

            if (input_state_L == False and input_state_R == False):
                GPIO.output(rled,1)
                GPIO.output(lled,1)
#                print(threading.enumerate())
                try:
                    tForward_stop.set()
                    if (tForward.is_alive()==True):
                        tForward.join()
                    tBackward_stop.set()
                    if (tBackward.is_alive()==True):
                        tBackward.join()
                except:
                    print('error occured')
                    print sys.exc_info()
                off()
            
            elif (input_state_L == False and input_state_R == True):
                GPIO.output(rled,0)
                GPIO.output(lled,1)
#                print "forward"
#                print (threading.enumerate())
                try:
                    if (tForward.is_alive()!=True):
#                        print ('start thread')
                        tForward_stop.clear()
#                        print tForward_stop.is_set()
                        tForward = threading.Thread(target = forward, args=(1, tForward_stop))
                        tForward.start()
#                        print (threading.enumerate())
                except:
                    print('error occured')
                    print sys.exc_info()
                    pass
            elif (input_state_R == False and input_state_L == True):
                GPIO.output(lled,0)
                GPIO.output(rled,1)
#                print "backward"
#                print (threading.enumerate())
                try:
                    if (tBackward.is_alive()!=True):
#                        print ('start thread')
                        tBackward_stop.clear()
#                        print tBackward_stop.is_set()
                        tBackward = threading.Thread(target = backward, args=(2, tBackward_stop))
                        tBackward.start()
#                        print (threading.enumerate())
                except:
                    print('error occured')
                    print sys.exc_info()
                    pass
            
            else:
                GPIO.output(lled,0)
                GPIO.output(rled,0)
#                print('button stopped')
#                print(threading.enumerate())
                try:
                    tForward_stop.set()
                    if (tForward.is_alive()==True):
                        tForward.join()
                    tBackward_stop.set()
                    if (tBackward.is_alive()==True):
                        tBackward.join()
                except:
                    print('error occured')
                    print sys.exc_info()
                off()

if __name__ == "__main__":
    main()
