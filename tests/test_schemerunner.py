import unittest   # The test framework
from water import controllers
from water import scheme

class Test_TestIncrementDecrement(unittest.TestCase):
    CONTROLLER = controllers.WaterController(17)
    SCHEME = scheme.WaterScheme()
    SEGMENT1 = scheme.BurstSegment(3, 2, 2)
    SEGMENT2 = scheme.IdleSegment(600)
    SEGMENT3 = scheme.BurstSegment(6, 2, 4)
    SEGMENT4 = scheme.IdleSegment(300)

    SCHEME.add(SEGMENT1)
    SCHEME.add(SEGMENT2)
    SCHEME.add(SEGMENT3)
    SCHEME.add(SEGMENT4)

    SCHEMERUNNER = scheme.SchemeRunner(CONTROLLER, SCHEME)

    def test_increment(self):
        try:
            SCHEMERUNNER.start(True)
            while SCHEMERUNNER.status != scheme.RunnerStatus.Idle:
                self.assertEqual(inc_dec.increment(3), 4)

        except KeyboardInterrupt:
            pass
        finally:
            print("stopping threads...")
            SCHEMERUNNER.stop()
            print("cleuning up GPIO...")
            CONTROLLER.cleanup()
            print("done and closed")

if __name__ == '__main__':
    unittest.main()