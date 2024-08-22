import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

pin = 23

GPIO.setup(pin, GPIO.IN)
   
def waterSensor():
    return GPIO.input(pin)
