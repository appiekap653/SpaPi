"""SpaPi: Sauna Control and Automatic Water Dispencer"""
import time
import sys
import RPi.GPIO as GPIO

GPIO.setwarnings(True)

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)

TIME_ON = 20
PARTS = 4
TIME_OFF = 300
PART_TIME = 3

try:
    while True:
        print("Water Running...")
        for i2 in range(PARTS, 0, -1):
            GPIO.output(17, GPIO.HIGH)
            for i in range(PART_TIME, 0, -1):
                sys.stdout.write(str(i)+' ')
                sys.stdout.flush()
                time.sleep(1)

            GPIO.output(17, GPIO.LOW)
            time.sleep(3)

        print("Water Stopping...")
        GPIO.output(17, GPIO.LOW)
        for i in range(TIME_OFF, 0, -1):
            sys.stdout.write(str(i)+' ')
            sys.stdout.flush()
            time.sleep(1)

except KeyboardInterrupt:
    GPIO.output(17, GPIO.LOW)
    GPIO.cleanup()
    print("exiting...")
