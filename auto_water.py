from gpiozero import *
from signal import pause

water_motor = LED(17)
#water_motor.blink(6, 240)
water_motor.on()
pause()

