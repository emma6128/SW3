#!/usr/bin/env python
# Halloween Ghost

import os
from pygame import mixer
import random
import RPi.GPIO as GPIO
import time

# set up assets folders
snd_dir = os.path.join(os.path.dirname(__file__), "wav")

# Set the GPIO naming convention
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

PinPIR = 12
bluePin = 11
# bluePin1 = 12
greenPin = 13
# greenPin1 = 16
redPin = 15
# redPin1 = 18

print("PIR Module Test (Ctrl-C to exit)")

# Set pin as input/output
GPIO.setup(PinPIR, GPIO.IN)

# Variables to hold current and last states
Current_State = 0
Previous_State = 0

def turnOff(pin):
    # GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)


def blink(pin):
    # GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)


def redOn():
    blink(redPin)
    # blink(redPin1)


def greenOn():
    blink(greenPin)
    # blink(greenPin1)


def blueOn():
    blink(bluePin)
    # blink(bluePin1)


def redOff():
    turnOff(redPin)
    # turnOff(redPin1)


def greenOff():
    turnOff(greenPin)
    # turnOff(greenPin1)


def blueOff():
    turnOff(bluePin)
    # turnOff(bluePin1)


try:
    print("Waiting for PIR to settle ...")
    # Loop until PIR output is zero
    while GPIO.input(PinPIR) == 1:
        Current_State = 0

    print("Ready")

    # Loop until user quits with Ctrl-C
    while True:
        # Read PIR state
        Current_State = GPIO.input(PinPIR)

        # If the PIR is triggered
        if Current_State == 1 and Previous_State == 0:
            print("Motion detected!")
                       
            # change to random colour
            redOn()
            greenOn()
            blueOn()
            print("LEDs On")
                        
            time.sleep(1)

            # Play random wav file from wav folder
            mixer.init()
            randomfile = random.choice(os.listdir(snd_dir))  # randomly choose wav file
            print(randomfile)  # debug
            file = snd_dir + "/" + randomfile
            print(file)  # debug
            a = mixer.Sound(file)
            print("length", a.get_length())  # debug
            mixer.Sound.play(mixer.Sound(file))  # Play selected wav file

            # Waits for the length of the sound + 1 second
            time.sleep(a.get_length() + 1)

            # Turn LEDs off
            redOff()
            greenOff()
            blueOff()
            print("LEDs Off")
            
            # Delay before PIR sensor reinitialises
            time.sleep(30)
            
            # Record previous state
            Previous_State = 1

        # If the PIR has returned to ready state
        elif Current_State == 0 and Previous_State == 1:
            print("Ready")
            Previous_State = 0

        # Wait for 10 milliseconds
        time.sleep(0.01)

except KeyboardInterrupt:
    print("Quit")

    # Reset GPIO settings
    GPIO.cleanup()

quit()
