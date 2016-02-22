#!/usr/bin/python
# 
# Creator     : Steven Cregan
# Date        : 02/21/16
# Description : This program will move a small vehicle forward 
#               and backwards as controlled by an Xbox360 wireless controller
import RPi.GPIO as GPIO
import time
import os, sys
import threading
# Credit to Zephod on github
# https://github.com/zephod/lego-pi
sys.path.insert(0, '/home/pi/')
from legopi.lib import xbox_read

GPIO.setmode(GPIO.BCM)
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
motorspeed = 8
delay = motorspeed/10000.0

# Just some wire colors for personal clarity
# blue
motorPin1 = 18
# white
motorPin2 = 23
# yellow
motorPin3 = 24
# orange
motorPin4 = 25

# Set the motor pins as output
GPIO.setup(motorPin1, GPIO.OUT)
GPIO.setup(motorPin2, GPIO.OUT)
GPIO.setup(motorPin3, GPIO.OUT)
GPIO.setup(motorPin4, GPIO.OUT)

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
    GPIO.output(motorPin1, w1)
    GPIO.output(motorPin2, w2)
    GPIO.output(motorPin3, w3)
    GPIO.output(motorPin4, w4)

# This function is here as a guarantee the motors will be
# released properly, with all pins set low
def off():
    setStep(0,0,0,0)
    time.sleep(delay)

def main():
    # Store controller values
    temp = ""
    A = 1
    B = 1
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
            temp = str(event)
            print temp
            input_state_L = GPIO.input(lbutton)
            input_state_R = GPIO.input(rbutton)
            print ("{0}  ,  {1}").format(input_state_L, input_state_R)
    
            if(temp == "Event(A,1,0)"):
                A = 0
                input_state_L = 0

            elif(temp == "Event(A,0,1)"):
                A = 1
                input_state_L = 1

            elif(temp == "Event(B,1,0)"):
                B = 0 
                input_state_R = 0

            elif(temp == "Event(B,0,1)"):
                B = 1
                input_state_R = 1

            else:
                input_state_L = A
                input_state_R = B
                pass
            input_state_L = A
            input_state_R = B

            print ("A = {0} , B = {1}").format(A, B)
            print ("{0}  ,  {1}").format(input_state_L, input_state_R)

            if (input_state_L == False and input_state_R == False):
                GPIO.output(rled,1)
                GPIO.output(lled,1)
                print(threading.enumerate())
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
                print "forward"
                print (threading.enumerate())
                try:
                    if (tForward.is_alive()!=True):
                        print ('start thread')
                        tForward_stop.clear()
                        print tForward_stop.is_set()
                        tForward = threading.Thread(target = forward, args=(1, tForward_stop))
                        tForward.start()
                        print (threading.enumerate())
                except:
                    print('error occured')
                    print sys.exc_info()
                    pass
            elif (input_state_R == False and input_state_L == True):
                GPIO.output(lled,0)
                GPIO.output(rled,1)
                print "backward"
                print (threading.enumerate())
                try:
                    if (tBackward.is_alive()!=True):
                        print ('start thread')
                        tBackward_stop.clear()
                        print tBackward_stop.is_set()
                        tBackward = threading.Thread(target = backward, args=(2, tBackward_stop))
                        tBackward.start()
                        print (threading.enumerate())
                except:
                    print('error occured')
                    print sys.exc_info()
                    pass
            
            else:
                GPIO.output(lled,0)
                GPIO.output(rled,0)
                print('button stopped')
                print(threading.enumerate())
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
