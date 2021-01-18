import RPi.GPIO as GPIO
import time
import signal
import sys
import os
import json
from statistics import mean
from count import getCount, setCount
        

# use Raspberry Pi board pin numbers
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
# set GPIO Pins
pinTrigger = 18
pinEcho = 24

setCount(0)
settings = json.load(open('settings.json'))
threshold = settings['threshold']
distance = threshold+1

def close(signal, frame):
        print("\nTurning off ultrasonic distance detection...\n")
        GPIO.cleanup() 
        sys.exit(0)

signal.signal(signal.SIGINT, close)

# set GPIO input and output channels
GPIO.setup(pinTrigger, GPIO.OUT)
GPIO.setup(pinEcho, GPIO.IN)

counted = False

def getMeasurement():
        # set Trigger to HIGH
        GPIO.output(pinTrigger, True)
        # set Trigger after 0.01ms to LOW
        time.sleep(0.00001)
        GPIO.output(pinTrigger, False)

        startTime = time.time()
        stopTime = time.time()

        # save start time
        while 0 == GPIO.input(pinEcho):
                startTime = time.time()

        # save time of arrival
        while 1 == GPIO.input(pinEcho):
                stopTime = time.time()

        # time difference between start and arrival
        TimeElapsed = stopTime - startTime
        # multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        distance = (TimeElapsed * 34300) / 2
        return distance

def getDistance(n=5):
        distances = [getMeasurement() for i in range(n)]
        return mean(distances)

while True:
        distance = getDistance()
        
        #print (f"Distance: {distance:.01f} cm")

        
        if(distance<=threshold and not counted):
                count = getCount()
                count += 1
                print(f'Current count is {count}')
                setCount(count)
                counted = True
        elif distance > threshold:
                counted = False
        else:
                #print(f"Sensor blocked, waiting to detect {threshold}cm; currently at {distance:.01f}cm")
                pass
        time.sleep(1)

