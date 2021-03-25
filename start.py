"""
SpaPi, Sauna and Automatic-Water control for RaspberryPi
"""
from spapi.water import scheme
from spapi import gpio_controller

CONTROLLER = gpio_controller.Controllers()
SCHEME = scheme.WaterScheme()

SEGMENT1 = scheme.BurstSegment(10, 4, 3)
SEGMENT2 = scheme.IdleSegment(240)
SEGMENT3 = scheme.BurstSegment(10, 4, 2)
SEGMENT4 = scheme.IdleSegment(240)

SCHEME.add(SEGMENT1)
SCHEME.add(SEGMENT2)
SCHEME.add(SEGMENT3)
SCHEME.add(SEGMENT4)

SCHEMERUNNER = scheme.SchemeRunner(CONTROLLER.watercontroller(), SCHEME)

try:
    SCHEMERUNNER.start(True)
    while SCHEMERUNNER.status != scheme.RunnerStatus.Idle:
        pass

except KeyboardInterrupt:
    pass
finally:
    print("stopping threads...")
    SCHEMERUNNER.stop()
    print("cleuning up GPIO...")
    CONTROLLER.cleanup()
    print("done and closed")
