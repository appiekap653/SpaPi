from gpiozero import *
from signal import pause

water_motor = DigitalOutputDevice(2)


def auto_water_on(on_time, off_time):
    water_motor.blink(on_time, off_time)


def auto_water_off():
    water_motor.off()
    water_motor.close()


auto_water_on(4, 240)
auto_water_off()

pause()
