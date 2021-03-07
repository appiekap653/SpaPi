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
SEGMENT2 = scheme.IdleSegment(480)
SEGMENT3 = scheme.BurstSegment(5, 2, 4)
SEGMENT4 = scheme.IdleSegment(300)

SCHEME.add(SEGMENT1)
SCHEME.add(SEGMENT2)
SCHEME.add(SEGMENT3)
SCHEME.add(SEGMENT4)

SCHEMERUNNER = scheme.SchemeRunner(CONTROLLER, SCHEME)

def run():
    SCHEMERUNNER.start(True)

try:
    t = Thread(target = run)
    t.start()
    time.sleep(4)
    SCHEMERUNNER.pause()
    time.sleep(15)
    SCHEMERUNNER.resume()
    t.join()

except KeyboardInterrupt:
    pass
finally:
    CONTROLLER.cleanup()
    print("exiting...")
