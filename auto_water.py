from gpiozero import *
from signal import pause

water_motor = LED(4)
water_motor.blink(4, 240)

pause()

