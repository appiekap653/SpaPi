"""
SpaPi, Sauna and Automatic-Water control for RaspberryPi
"""
import time

from threading import Thread
from water import controllers
from water import scheme

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

try:
    SCHEMERUNNER.start(True)
    while SCHEMERUNNER.running:
        pass

except KeyboardInterrupt:
    pass
finally:
    SCHEMERUNNER.stop()
    CONTROLLER.cleanup()
    print("exiting...")
