#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import sys
GPIO.setmode(GPIO.BCM)

motorspeed = 1
delay = motorspeed/1000.0

#blue
motor1Pin1 = 15
#white
motor1Pin2 = 18
#yellow
motor1Pin3 = 23
#orange
motor1Pin4 = 24

GPIO.setup(motor1Pin1, GPIO.OUT)
GPIO.setup(motor1Pin2, GPIO.OUT)
GPIO.setup(motor1Pin3, GPIO.OUT)
GPIO.setup(motor1Pin4, GPIO.OUT)

#blue
motor2Pin1 = 25
#white
motor2Pin2 = 8
#yellow
motor2Pin3 = 7
#orange
motor2Pin4 = 12

GPIO.setup(motor2Pin1, GPIO.OUT)
GPIO.setup(motor2Pin2, GPIO.OUT)
GPIO.setup(motor2Pin3, GPIO.OUT)
GPIO.setup(motor2Pin4, GPIO.OUT)

#blue
motor3Pin1 = 22
#white
motor3Pin2 = 27
#yellow
motor3Pin3 = 17
#orange
motor3Pin4 = 4

GPIO.setup(motor3Pin1, GPIO.OUT)
GPIO.setup(motor3Pin2, GPIO.OUT)
GPIO.setup(motor3Pin3, GPIO.OUT)
GPIO.setup(motor3Pin4, GPIO.OUT)

#blue
motor4Pin1 = 19
#white
motor4Pin2 = 13
#yellow
motor4Pin3 = 6
#orange
motor4Pin4 = 5

GPIO.setup(motor4Pin1, GPIO.OUT)
GPIO.setup(motor4Pin2, GPIO.OUT)
GPIO.setup(motor4Pin3, GPIO.OUT)
GPIO.setup(motor4Pin4, GPIO.OUT)

#blue
motor5Pin1 = 3
#white
motor5Pin2 = 7
#yellow
motor5Pin3 = 8
#orange
motor5Pin4 = 26

GPIO.setup(motor5Pin1, GPIO.OUT)
GPIO.setup(motor5Pin2, GPIO.OUT)
GPIO.setup(motor5Pin3, GPIO.OUT)
GPIO.setup(motor5Pin4, GPIO.OUT)

input = ""
multiaxis = [""]


def backward(axis, steps):
  for i in range(0, steps):
    time.sleep(delay)
    setStep(axis,1,0,0,0)
    time.sleep(delay)
    setStep(axis,1,0,0,1)
    time.sleep(delay)
    setStep(axis,0,0,0,1)
    time.sleep(delay)
    setStep(axis,0,0,1,1)
    time.sleep(delay)
    setStep(axis,0,0,1,0)
    time.sleep(delay)
    setStep(axis,0,1,1,0)
    time.sleep(delay)
    setStep(axis,0,1,0,0)
    time.sleep(delay)
    setStep(axis,1,1,0,0)
    time.sleep(delay)

def forward(axis, steps):
  for i in range(0, steps):
    time.sleep(delay)
    setStep(axis,1,0,0,0)
    time.sleep(delay)
    setStep(axis,1,1,0,0)
    time.sleep(delay)
    setStep(axis,0,1,0,0)
    time.sleep(delay)
    setStep(axis,0,1,1,0)
    time.sleep(delay)
    setStep(axis,0,0,1,0)
    time.sleep(delay)
    setStep(axis,0,0,1,1)
    time.sleep(delay)
    setStep(axis,0,0,0,1)
    time.sleep(delay)
    setStep(axis,1,0,0,1)
    time.sleep(delay)

def setStep(axis, w1, w2, w3, w4):
  if(axis == "x" or axis == "X"):
    GPIO.output(motor1Pin1, w1)
    GPIO.output(motor1Pin2, w2)
    GPIO.output(motor1Pin3, w3)
    GPIO.output(motor1Pin4, w4)
  elif(axis == "y" or axis == "Y"):
    GPIO.output(motor2Pin1, w1)
    GPIO.output(motor2Pin2, w2)
    GPIO.output(motor2Pin3, w3)
    GPIO.output(motor2Pin4, w4)
  elif(axis == "z" or axis == "Z"):
    GPIO.output(motor3Pin1, w1)
    GPIO.output(motor3Pin2, w2)
    GPIO.output(motor3Pin3, w3)
    GPIO.output(motor3Pin4, w4)
  elif(axis == "a" or axis == "A"):
    GPIO.output(motor4Pin1, w1)
    GPIO.output(motor4Pin2, w2)
    GPIO.output(motor4Pin3, w3)
    GPIO.output(motor4Pin4, w4)
  elif(axis == "b" or axis == "B"):
    GPIO.output(motor5Pin1, w1)
    GPIO.output(motor5Pin2, w2)
    GPIO.output(motor5Pin3, w3)
    GPIO.output(motor5Pin4, w4)


def off():
  setStep("x",0,0,0,0)
  setStep("y",0,0,0,0)
  setStep("z",0,0,0,0)
  setStep("a",0,0,0,0)
  setStep("b",0,0,0,0)
  time.sleep(delay)

while True:
  try:
	input = raw_input("What axis: ")
	if(len(input)>1):
	  for x in ([x.strip() for x in str(input).split(',')]):
	    multiaxis.append(x)
	    print(str(x))
	  forwardstep = raw_input("How many steps forward: ")
	  backwardstep = raw_input("How many steps backward: ")
	  for j in range(0,int(forwardstep)):
	    for k in multiaxis:	
	      forward(str(k), (1))
	  for j in range(0,int(backwardstep)):
	    for k in multiaxis:
	      backward(str(k), (1))
	  multiaxis = [""]
	  off()
	  input = ""
	  forwardstep = ""
	  backwardstep = ""
	else:
	  forwardstep =raw_input("How many steps forward:")
	  backwardstep = raw_input("How many steps backward: ")
	  forward(str(input), int(forwardstep))
	  backward(str(input), int(backwardstep)) 
          off()
  except(KeyboardInterrupt, SystemExit):
        print '\nKeyboardInterrupt!'
        off()
	GPIO.cleanup()
	sys.exit()
