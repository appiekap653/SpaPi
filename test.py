import RPi.GPIO as GPIO
from signal import pause
import time
import sys

GPIO.setwarnings(True)

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)

time_on=20;
parts=4;
time_off=300;
part_time=3;

try:
    while True:
        print("Water Running...")
        for i2 in range(parts,0,-1):
            GPIO.output(17, GPIO.HIGH)
            for i in range(part_time,0,-1):
                sys.stdout.write(str(i)+' ')
                sys.stdout.flush()
                time.sleep(1)
                
            GPIO.output(17, GPIO.LOW)   
            time.sleep(3)
            
        print("Water Stopping...")
        GPIO.output(17, GPIO.LOW)
        for i in range(time_off,0,-1):
            sys.stdout.write(str(i)+' ')
            sys.stdout.flush()
            time.sleep(1)

except KeyboardInterrupt:
    GPIO.output(17, GPIO.LOW)
    GPIO.cleanup()
    print("exiting...")
