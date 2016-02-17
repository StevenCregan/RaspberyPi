#!/usr/bin/python
import RPi.GPIO as GPIO import time

#This script takes input from the GPIO pins.
#There are two buttons used for input.
#LED's are used to indicate which button is pressed.
#When the buttons are pressed, they cause stepper motors
#to rotate in a specified direction

#GPIO declarations
GPIO.setmode(GPIO.BCM)
lbutton = 26
rbutton = 19
GPIO.setup(lbutton, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(rbutton, GPIO.IN, pull_up_down=GPIO.PUD_UP)
lled = 6
rled = 13
GPIO.setup(lled, GPIO.OUT)
GPIO.setup(rled, GPIO.OUT)

#for the current motors, set the max speed
motorspeed = 8
delay = motorspeed/10000.0

#Wiring Colors and pins
#blue
motorPin1 = 18
#white
motorPin2 = 23
#yellow
motorPin3 = 24
#orange
motorPin4 = 25

#GPIO setup
GPIO.setup(motorPin1, GPIO.OUT)
GPIO.setup(motorPin2, GPIO.OUT)
GPIO.setup(motorPin3, GPIO.OUT)
GPIO.setup(motorPin4, GPIO.OUT)

#Setting the stepper motors to rotate at the specified speed
def backward():
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

def forward():
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

#setStep will set output pins to high/low volt
def setStep(w1, w2, w3, w4):
  GPIO.output(motorPin1, w1)
  GPIO.output(motorPin2, w2)
  GPIO.output(motorPin3, w3)
  GPIO.output(motorPin4, w4)

#just incase, a method to turn off all motors
def off():
  setStep(0,0,0,0)
  time.sleep(delay)

#main process loop
if __name__ == "__main__":
    while True:
        input_state_L = GPIO.input(lbutton)
        input_state_R = GPIO.input(rbutton)

        if (input_state_L == False and input_state_R == False):
            GPIO.output(rled,1)
            GPIO.output(lled,1)
            off()

        elif (input_state_L == False and input_state_R == True):
            GPIO.output(rled,0)
            GPIO.output(lled,1)
            forward()
        elif (input_state_R == False and input_state_L == True):
            GPIO.output(lled,0)
            GPIO.output(rled,1)
            backward()
        else:
            GPIO.output(lled,0)
            GPIO.output(rled,0)
            off()
