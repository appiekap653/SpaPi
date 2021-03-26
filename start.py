"""
SpaPi, Sauna and Automatic-Water control for RaspberryPi
"""
from spapi.sauna import thermometer
from spapi.water import scheme
from spapi import gpio

CONTROLLER = gpio.GPIOController()

THERMDEVICE = thermometer.DS18B20(4, True, CONTROLLER)
THERMOMETER = thermometer.Thermometer(THERMDEVICE, 2)

SCHEME = scheme.WaterScheme()

SEGMENT1 = scheme.BurstSegment(10, 5, 2)
SEGMENT2 = scheme.IdleSegment(600)
SEGMENT3 = scheme.BurstSegment(10, 5, 2)
SEGMENT4 = scheme.IdleSegment(300)

SCHEME.add(SEGMENT1)
SCHEME.add(SEGMENT2)
SCHEME.add(SEGMENT3)
SCHEME.add(SEGMENT4)

SCHEMERUNNER = scheme.SchemeRunner(CONTROLLER.watercontroller(), SCHEME)

try:
    SCHEMERUNNER.start(True)
    CURRENT_SEGMENT = SCHEMERUNNER.current_segment

    while SCHEMERUNNER.status != scheme.RunnerStatus.Idle:
        if CURRENT_SEGMENT != SCHEMERUNNER.current_segment:
            CURRENT_SEGMENT = SCHEMERUNNER.current_segment
            print("Temperature: {}".format(THERMOMETER.temperature))

except KeyboardInterrupt:
    pass
finally:
    print("stopping threads...")
    SCHEMERUNNER.stop()
    CONTROLLER.cleanup()
    print("done and closed")
