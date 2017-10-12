# CamJam Edukit 2 - Sensors
# Worksheet 6 - Alarm

#Import Python header files
import RPi.GPIO as GPIO
import time

# Set the GPIO naming convention
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

PinPIR = 17
PinRedLED = 18
PinBlueLED = 24
PinBuzzer = 22

print("PIR Module Test (Ctrl-C to exit)")

# Set pin as input/output
GPIO.setup(PinPIR, GPIO.IN)
GPIO.setup(PinRedLED, GPIO.OUT)
GPIO.setup(PinBlueLED, GPIO.OUT)
GPIO.setup(PinBuzzer, GPIO.OUT)

# Variables to hold current and last states
Current_State = 0
Previous_State = 0

try:
    print("Waiting for PIR to settle ...")
    # Loop until PIR output is zero
    while GPIO.input(PinPIR)==1:
        Current_State = 0
        
    print("Ready")
    
    # Loop until user quits with Ctrl-C
    while True:
        # Read PIR state
        Current_State = GPIO.input(PinPIR)
        
        # If the PIR is triggered
        if Current_State==1 and Previous_State==0:
            print("Motion detected!")
            # Turn on lights and sound buzzer
            GPIO.output(PinBuzzer, GPIO.HIGH)
            GPIO.output(PinRedLED, GPIO.HIGH)
            GPIO.output(PinBlueLED, GPIO.HIGH)
            time.sleep(5)
            GPIO.output(PinBlueLED, GPIO.LOW)
            GPIO.output(PinBuzzer, GPIO.LOW)
            GPIO.output(PinRedLED, GPIO.LOW)
                
            # Record previous state
            Previous_State=1
            
        # If the PIR has returned to ready state
        elif Current_State==0 and Previous_State==1:
            print("Ready")
            Previous_State=0
            
        # Wait for 10 milliseconds
        time.sleep(0.01)
        
except KeyboardInterrupt:
    print("Quit")
    
    # Reset GPIO settings
    GPIO.cleanup()