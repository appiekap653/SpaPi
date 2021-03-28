import unittest   # The test framework
import time
from spapi.sauna import thermometer
from spapi import gpio

class Test_Thermometer(unittest.TestCase):

    def setUp(self):
        self._controller = gpio.GPIOController()

    def tearDown(self):
        self._controller.cleanup()

    def test_DS18B20_temperature_value(self):
        thermdevice = thermometer.DS18B20(4, True, self._controller)
        therm = thermometer.Thermometer(thermdevice)
        time.sleep(5)
        self.assertIsNotNone(therm.temperature)
        print("DS18B20 Temperature: {}".format(therm.temperature))
        self.assertNotEqual(therm.temperature, 999.9)

    def test_DHT22_temperature_value(self):
        thermdevice = thermometer.DHT22(18, False, self._controller)
        therm = thermometer.Thermometer(thermdevice)
        time.sleep(5)
        self.assertIsNotNone(therm.temperature)
        print("DHT22 Temperature: {}".format(therm.temperature))
        self.assertNotEqual(therm.temperature, 999.9)

    def test_DHT22_humidity_value(self):
        thermdevice = thermometer.DHT22(18, False, self._controller)
        therm = thermometer.Thermometer(thermdevice)
        time.sleep(5)
        self.assertIsNotNone(therm.humidity)
        print("DHT22 Humidity: {}".format(therm.humidity))
        self.assertNotEqual(therm.humidity, 0.0)

if __name__ == '__main__':
    unittest.main()
