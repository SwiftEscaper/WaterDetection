import RPi.GPIO as GPIO
import time

# 192.168.219.103

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

pin = 23

GPIO.setup(pin, GPIO.IN)

try:
    while True:
        input = GPIO.input(pin)
        print(input)
        time.sleep(1.0)
        
except KeyboardInterrupt:
    GPIO.cleanup()