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
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)


def blink(pin):
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)


def redOn():
    blink(redPin)


def greenOn():
    blink(greenPin)


def blueOn():
    blink(bluePin)


def yellowOn():
    blink(redPin)
    blink(greenPin)


def magentaOn():
    blink(bluePin)
    blink(redPin)


def cyanOn():
    blink(bluePin)
    blink(greenPin)


def whiteOn():
    blink(redPin)
    blink(greenPin)
    blink(bluePin)


def redOff():
    turnOff(redPin)


def greenOff():
    turnOff(greenPin)


def blueOff():
    turnOff(bluePin)


def yellowOff():
    turnOff(redPin)
    turnOff(greenPin)


def magentaOff():
    turnOff(bluePin)
    turnOff(redPin)


def cyanOff():
    turnOff(bluePin)
    turnOff(greenPin)


def whiteOff():
    turnOff(redPin)
    turnOff(greenPin)
    turnOff(bluePin)


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

            # select a random colour
            colourlist = [redOn, greenOn, blueOn, yellowOn,
                          magentaOn, cyanOn, whiteOn]
            randColour = random.choice(colourlist)
            print(randColour)
            randColour()
            print("LEDs On")

            time.sleep(1)

            # Play random wav file from wav folder
            mixer.init()
            # randomly choose wav file
            randomfile = random.choice(os.listdir(snd_dir))
            print(randomfile)  # debug
            file = snd_dir + "/" + randomfile
            print(file)  # debug
            a = mixer.Sound(file)
            print("length", a.get_length())  # debug
            mixer.Sound.play(mixer.Sound(file))  # Play selected wav file

            # Waits for the length of the sound + 1 second
            time.sleep(a.get_length() + 1)

            # Turn LEDs off
            if randColour == redOn:
                redOff()
            elif randColour == greenOn:
                greenOff()
            elif randColour == blueOn:
                blueOff()
            elif randColour == yellowOn:
                yellowOff()
            elif randColour == magentaOn:
                magentaOff()
            elif randColour == cyanOn:
                cyanOff()
            elif randColour == whiteOn:
                whiteOff()
            else:
                print("err in colour turnOff")
            print("LEDs Off")

            # Delay before PIR sensor reinitialises
            time.sleep(10)

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
