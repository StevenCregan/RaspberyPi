#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import sys
GPIO.setmode(GPIO.BCM)

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

def forward(delay, steps):
  for i in range(0, steps):
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

def backward(delay, steps):
  for i in range(0, steps):
    setStep(1,0,1,0)
    time.sleep(delay)
    setStep(0,1,0,1)
    time.sleep(delay)
    setStep(0,1,1,0)
    time.sleep(delay)
    setStep(1,0,1,0)
    time.sleep(delay)

def setStep(w1, w2, w3, w4):
  GPIO.output(motorPin1, w1)
  GPIO.output(motorPin2, w2)
  GPIO.output(motorPin3, w3)
  GPIO.output(motorPin4, w4)

while True:
  try:
    delay = raw_input("enter delay: ")
    steps = raw_input("enter steps: ")
    forward(int(delay)/10000.0, int(steps))
  except(KeyboardInterrupt, SystemExit):
    print '\nKeyboardInterrupt!'
    sys.exit()
