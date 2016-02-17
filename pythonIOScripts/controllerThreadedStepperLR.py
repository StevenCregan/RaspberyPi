#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import os, sys
from multiprocessing import Process
sys.path.insert(0, '/home/pi/')
from legopi.lib import xbox_read
GPIO.setmode(GPIO.BCM)

lbutton = 26
rbutton = 19
GPIO.setup(lbutton, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(rbutton, GPIO.IN, pull_up_down=GPIO.PUD_UP)
lled = 6
rled = 13
GPIO.setup(lled, GPIO.OUT)
GPIO.setup(rled, GPIO.OUT)

motorspeed = 8
delay = motorspeed/10000.0

#blue
motorPin1 = 18
#white
motorPin2 = 23
#yellow
motorPin3 = 24
#orange
motorPin4 = 25

GPIO.setup(motorPin1, GPIO.OUT)
GPIO.setup(motorPin2, GPIO.OUT)
GPIO.setup(motorPin3, GPIO.OUT)
GPIO.setup(motorPin4, GPIO.OUT)

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
  while True:
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

def setStep(w1, w2, w3, w4):
    GPIO.output(motorPin1, w1)
    GPIO.output(motorPin2, w2)
    GPIO.output(motorPin3, w3)
    GPIO.output(motorPin4, w4)

def off():
  setStep(0,0,0,0)
  time.sleep(delay)

if __name__ == "__main__":
  temp = ""
  pForward = Process(target=forward)
  while True:
   for event in xbox_read.event_stream(deadzone=12000):
    temp = str(event)
    print temp
    
    input_state_L = GPIO.input(lbutton)
    input_state_R = GPIO.input(rbutton)
    print ("{0}  ,  {1}").format(input_state_L, input_state_R)
    
    if(temp == "Event(A,1,0)"):
        input_state_L = 0
    else:
        input_state_L = 1
    
    print ("{0}  ,  {1}").format(input_state_L, input_state_R)

    if (input_state_L == False and input_state_R == False):
        GPIO.output(rled,1)
        GPIO.output(lled,1)
        off()

    elif (input_state_L == False and input_state_R == True):
        GPIO.output(rled,0)
        GPIO.output(lled,1)
        #forward()
        print "forward"
        if (pForward.is_alive()!=True):
          pForward.start()
        time.sleep(0.1)
#        pForward.terminate()
        time.sleep(0.1)
        print pForward, pForward.is_alive()
    elif (input_state_R == False and input_state_L == True):
        GPIO.output(lled,0)
        GPIO.output(rled,1)
        backward()
        print "backward"
    else:
        GPIO.output(lled,0)
        GPIO.output(rled,0)
        off()
