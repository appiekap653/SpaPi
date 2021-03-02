"""SpaPi: Sauna Control and Automatic Water Dispencer"""
import time
import RPi.GPIO as GPIO

GPIO.setwarnings(True)

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)

TIME_ON = 20
TIME_OFF = 300
PARTS = 4
PART_ON_TIME = 3
PART_OFF_TIME = 3

try:
    while True:
        print("Water Running...")
        for i2 in range(PARTS, 0, -1):
            GPIO.output(17, GPIO.HIGH)
            for i in range(PART_ON_TIME, 0, -1):
                print(i, flush=True)
                time.sleep(1)

            GPIO.output(17, GPIO.LOW)
            time.sleep(PART_OFF_TIME)

        print("Water Stopping...")
        GPIO.output(17, GPIO.LOW)
        for i in range(TIME_OFF, 0, -1):
            print(i, flush=True)
            time.sleep(1)

except KeyboardInterrupt:
    GPIO.output(17, GPIO.LOW)
    GPIO.cleanup()
    print("exiting...")
finally:
    GPIO.output(17, GPIO.LOW)
    GPIO.cleanup()
    print("exiting...")
