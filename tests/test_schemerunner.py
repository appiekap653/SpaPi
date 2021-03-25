import unittest   # The test framework
from unittest.mock import patch, MagicMock
from spapi.water import scheme
from spapi import gpio_controller

class Test_TestSchemeRunner(unittest.TestCase):
    patcher = None

    def setUpModule(self):
        MockRPi = MagicMock()
        modules = {
            "RPi": MockRPi,
            "RPi.GPIO": MockRPi.GPIO
        }
        self.patcher = patch.dict("sys.modules", modules)
        self.patcher.start()

    @patch("spapi.gpio_controller.Controllers", autospec=True)
    def setUp(self, mock_watercontroller):
        self.CONTROLLER = gpio_controller.Controllers()
        self.SCHEME = scheme.WaterScheme()
        self.SEGMENT1 = scheme.BurstSegment(3, 2, 2)
        self.SEGMENT2 = scheme.IdleSegment(600)
        self.SEGMENT3 = scheme.BurstSegment(3, 2, 2)
        self.SEGMENT4 = scheme.IdleSegment(1)

        self.SCHEME.add(self.SEGMENT1)
        self.SCHEME.add(self.SEGMENT2)
        self.SCHEME.add(self.SEGMENT3)
        self.SCHEME.add(self.SEGMENT4)

        self.SCHEMERUNNER = scheme.SchemeRunner(self.CONTROLLER.watercontroller(), self.SCHEME)

    def tearDown(self):
        self.CONTROLLER.cleanup()

    def tearDownModule(self):
        self.patcher.stop()

    @patch("spapi.sauna.thermometer.read_temp", autospec=True)
    def test_status_running(self, mock_therm):
        self.SCHEMERUNNER.start(True)
        while self.SCHEMERUNNER.status != scheme.RunnerStatus.Idle:
            self.assertEqual(self.SCHEMERUNNER.status, scheme.RunnerStatus.Running)
            self.SCHEMERUNNER.pause()
            self.assertEqual(self.SCHEMERUNNER.status, scheme.RunnerStatus.Paused)
            self.SCHEMERUNNER.resume()
            self.assertEqual(self.SCHEMERUNNER.status, scheme.RunnerStatus.Running)
        self.assertEqual(self.SCHEMERUNNER.status, scheme.RunnerStatus.Running)
        self.SCHEMERUNNER.stop()

if __name__ == '__main__':
    unittest.main()
