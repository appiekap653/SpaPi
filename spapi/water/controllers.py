"""
The WaterController class takes care of the actual
GPIO outputs to turn the water motor on or off
"""
import RPi.GPIO as GPIO

class WaterController:
    """
    Constructor to set GPIO pin
    """
    def __init__(self, gpio_pin):
        self._gpio_pin = gpio_pin

        GPIO.setwarnings(True)

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._gpio_pin, GPIO.OUT)

    def water_on(self):
        """Turn water motor on"""
        GPIO.output(self._gpio_pin, GPIO.HIGH)

    def water_off(self):
        """Turn water motor off"""
        GPIO.output(self._gpio_pin, GPIO.LOW)

    def cleanup(self):
        """Clean up GPIO"""
        GPIO.output(self._gpio_pin, GPIO.LOW)
        GPIO.cleanup()
