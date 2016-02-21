#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import os, sys
from multiprocessing import Process
import threading
# Credit to Zephod on github
# https://github.com/zephod/lego-pi
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

def setStep(w1, w2, w3, w4):
    GPIO.output(motorPin1, w1)
    GPIO.output(motorPin2, w2)
    GPIO.output(motorPin3, w3)
    GPIO.output(motorPin4, w4)

def off():
  setStep(0,0,0,0)
  time.sleep(delay)

if __name__ == "__main__":
  #store controller values
  temp = ""
  A = 1
  pForward = Process(target=forward)
  tForward_stop = threading.Event()
  tForward = threading.Thread(target = forward, args=(1, tForward_stop))
  tForward.daemon = True
  while True:
   for event in xbox_read.event_stream(deadzone=12000):
    temp = str(event)
    print temp
    print A
    input_state_L = GPIO.input(lbutton)
    input_state_R = GPIO.input(rbutton)
    print ("{0}  ,  {1}").format(input_state_L, input_state_R)
    
    if(temp == "Event(A,1,0)"):
        A = 0
        input_state_L = 0
    elif(temp == "Event(A,0,1)"):
        A = 1
        input_state_L = 1
    else:
        input_state_L = A
        pass
        
    print input_state_L
    print ("{0}  ,  {1}").format(input_state_L, input_state_R)

    if (input_state_L == False and input_state_R == False):
        GPIO.output(rled,1)
        GPIO.output(lled,1)
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
        backward()
        print "backward"
    else:
        GPIO.output(lled,0)
        GPIO.output(rled,0)
        print('button stopped')
        print(threading.enumerate())
        try:
#          if (tForward.is_alive()==True):
            tForward_stop.set()
            tForward.join()
        except:
          print('error occured')
          print sys.exc_info()
        off()
