"""
The GPIO_Controller class takes care of the actual
GPIO outputs to turn all hardware on or off
"""
from abc import ABC, abstractmethod
from threading import Lock
import RPi.GPIO as GPIO

class SingletonMeta(type):
    """
    This is a thread-safe implementation of Singleton.
    """

    _instances = {}

    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]

class WaterController(metaclass=SingletonMeta):
    """
    The WaterController class takes care of the actual
    GPIO outputs to turn the water motor on or off
    """

    def __init__(self, gpio_pin):
        self._gpio_pin = gpio_pin
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

class ThermometerController(metaclass=SingletonMeta):
    """
    The Thermometer class takes care of the actual
    GPIO outputs to read the tempurature
    """

    _gpio_pin = 0
    _pull_up_set = 0

    def __init__(self, gpio_pin):
        self._gpio_pin = gpio_pin

        if self._pull_up_set == 0:
            GPIO.setup(self._gpio_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            self._pull_up_set = 1

class Controllers(metaclass=SingletonMeta):
    """
    Sigleton Factory Class to give access to
    every controllers
    """
    _pin_watermotor = 17
    _pin_thermometer = 4

    def __init__(self):
        GPIO.setwarnings(True)
        GPIO.setmode(GPIO.BCM)

    @classmethod
    def watercontroller(cls) -> WaterController:
        return WaterController(cls._pin_watermotor)

    @classmethod
    def thermometercontroller(cls) -> ThermometerController:
        return ThermometerController(cls._pin_thermometer)

    @classmethod
    def cleanup(cls):
        """Clean up GPIO"""
        cls.watercontroller().cleanup()
        GPIO.cleanup()

class ControllerManager():
    pass
