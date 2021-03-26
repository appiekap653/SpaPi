"""
The GPIO_Controller class takes care of the actual
GPIO outputs to turn all hardware on or off
"""
from abc import ABC, abstractmethod
from threading import Lock
from enum import Enum
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

class PullUpDown(Enum):
    """Representation of Pull UP/DOWN/OFF for GPIO pins"""
    PUD_OFF = 0
    PUD_UP = 1
    PUD_DOWN = 2

class GPIOController(metaclass=SingletonMeta):
    """
    Sigleton Factory Class to give access to
    every controllers
    """
    _pin_watermotor = 17

    _inputs = []
    _outputs = []

    def __init__(self):
        GPIO.setwarnings(True)
        GPIO.setmode(GPIO.BCM)

    def setup_input(self, pin: int, pull_up: PullUpDown):
        #TODO make sure only one pin is used at the same time
        #TODO create better way to store in and output information
        _pin = pin
        _pull_up = pull_up

        if _pull_up == PullUpDown.PUD_UP:
            GPIO.setup(_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        elif _pull_up == PullUpDown.PUD_DOWN:
            GPIO.setup(_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        else:
            GPIO.setup(_pin, GPIO.IN, pull_up_down=GPIO.PUD_OFF)

        self._inputs.append(_pin)

    @classmethod
    def watercontroller(cls) -> WaterController:
        return WaterController(cls._pin_watermotor)

    @classmethod
    def cleanup(cls):
        """Clean up GPIO"""
        print("cleaning up GPIO...")
        cls.watercontroller().cleanup()
        GPIO.cleanup()
