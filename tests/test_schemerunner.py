import unittest   # The test framework
from unittest.mock import patch, MagicMock
from spapi.water import controllers
from spapi.water import scheme

class Test_TestSchemeRunner(unittest.TestCase):

    def setUpModule():
        MockRPi = MagicMock()
        modules = {
            "RPi": MockRPi,
            "RPi.GPIO": MockRPi.GPIO
        }
        patcher = patch.dict("sys.modules", modules)
        patcher.start()

    @patch("spapi.water.controllers.WaterController", autospec=True)
    def setUp(self, mock_watercontroller):
        self.CONTROLLER = controllers.WaterController(17)
        self.SCHEME = scheme.WaterScheme()
        self.SEGMENT1 = scheme.BurstSegment(3, 2, 2)
        self.SEGMENT2 = scheme.IdleSegment(600)
        self.SEGMENT3 = scheme.BurstSegment(3, 2, 2)
        self.SEGMENT4 = scheme.IdleSegment(1)

        self.SCHEME.add(self.SEGMENT1)
        self.SCHEME.add(self.SEGMENT2)
        self.SCHEME.add(self.SEGMENT3)
        self.SCHEME.add(self.SEGMENT4)

        self.SCHEMERUNNER = scheme.SchemeRunner(self.CONTROLLER, self.SCHEME)

    def tearDown(self):
        self.CONTROLLER.cleanup()

    def teardownModule():
        patcher.stop()

    @patch("spapi.sauna.thermometer.read_temp", autospec=True)
    def test_status_running(self, mock_therm):
        self.SCHEMERUNNER.start(True)
        while self.SCHEMERUNNER.status != scheme.RunnerStatus.Idle:
            pass
        self.assertEqual(self.SCHEMERUNNER.status, scheme.RunnerStatus.Running)
        self.SCHEMERUNNER.stop()

if __name__ == '__main__':
    unittest.main()
