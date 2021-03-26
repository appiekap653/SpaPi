import unittest   # The test framework
import time
from spapi.sauna import thermometer
from spapi import gpio

class Test_TestThermometer(unittest.TestCase):

    def setUp(self):
        self._controller = gpio.GPIOController()
        self._thermdevice = thermometer.DS18B20(4, True, self._controller)
        self._thermometer = thermometer.Thermometer(self._thermdevice, 2)

    def tearDown(self):
        self._controller.cleanup()

    def test_temperature_value(self):
        time.sleep(5)
        self.assertIsNotNone(self._thermometer.temperature)
        print("Temperature: {}".format(self._thermometer.temperature))
        self.assertNotEqual(self._thermometer.temperature, 999.9)

if __name__ == '__main__':
    unittest.main()
