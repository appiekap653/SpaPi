"""Read temperture values from DS18B20"""
import glob
import time
from abc import ABC, abstractmethod
from threading import Thread
from spapi import gpio

class ThermDevice(ABC):

    def __init__(self, pin: int, pull_up: bool, controller: gpio.GPIOController):
        self._pin_number = pin
        self._pull_up = pull_up
        self._controller = controller

    @abstractmethod
    def setup(self):
        pass

    @abstractmethod
    def read_temp(self) -> float:
        pass

    @property
    def pin(self) -> int:
        return self._pin_number

    @property
    def pull_up(self) -> bool:
        return self._pull_up

class DS18B20(ThermDevice):

    def setup(self):
        if self._pull_up:
            self._controller.setup_input(self._pin_number, gpio.PullUpDown.PUD_UP)
        else:
            self._controller.setup_input(self._pin_number, gpio.PullUpDown.PUD_OFF)

    def read_temp(self) -> float:
        for sensor in glob.glob("/sys/bus/w1/devices/w1_bus_master1/28-*/w1_slave"):
            try:
                sfile = open(sensor, 'r')
                data = sfile.read()
                sfile.close()

                if "YES" in data:
                    (discard, sep, reading) = data.partition(' t=')
                    temp_c = float(reading) / 1000.0
                    return temp_c
                return 999.9
            except:
                return 999.9

class Thermometer:

    _temperature = 999.9

    def __init__(self, device: ThermDevice, interval: int):
        self._therm_device = device
        self._interval = interval

        self._therm_device.setup()

        self._thread = Thread(target=self._thread_task)
        self._thread.daemon = True
        self._thread.start()

    def _thread_task(self):
        while True:
            self._temperature = self._therm_device.read_temp()
            time.sleep(self._interval)

    @property
    def device(self):
        return self._therm_device

    @property
    def temperature(self) -> float:
        return self._temperature
