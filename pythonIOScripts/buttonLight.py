#!/usr/bin/python
import RPi.GPIO as GPIO
import time

#this script takes input from two buttons
#it lights up LED's based on which button is being pressed

#GPIO Declarations
GPIO.setmode(GPIO.BCM)
lbutton = 26
rbutton = 19
GPIO.setup(lbutton, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(rbutton, GPIO.IN, pull_up_down=GPIO.PUD_UP)
lled = 6
rled = 13
GPIO.setup(lled, GPIO.OUT)
GPIO.setup(rled, GPIO.OUT)

while True:
     
	input_state_L = GPIO.input(lbutton)
        input_state_R = GPIO.input(rbutton)

	if (input_state_L == False):
	  GPIO.output(rled,0)
          GPIO.output(lled,1)
        if input_state_R == False:
          GPIO.output(lled,0)
          GPIO.output(rled,1)
          

	else:
		GPIO.output(lled,0)
                GPIO.output(rled,0)
