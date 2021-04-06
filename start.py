"""
SpaPi, Sauna and Automatic-Water control for RaspberryPi
"""
from spapi.sauna import thermometer
from spapi.water import scheme
from spapi import gpio
from spapi.sauna import display

CONTROLLER = gpio.GPIOController()

THERMDEVICE = thermometer.DS18B20(CONTROLLER, 4, True)
THERMOMETER = thermometer.Thermometer(THERMDEVICE)

THERMDEVICEDHT = thermometer.DHT22(CONTROLLER, 18)
THERMOMETERDHT = thermometer.Thermometer(THERMDEVICEDHT)

SCHEME = scheme.WaterScheme()

SEGMENT1 = scheme.BurstSegment(10, 5, 3)
SEGMENT2 = scheme.IdleSegment(300)
SEGMENT3 = scheme.BurstSegment(10, 5, 3)
SEGMENT4 = scheme.IdleSegment(300)

SCHEME.add(SEGMENT1)
SCHEME.add(SEGMENT2)
SCHEME.add(SEGMENT3)
SCHEME.add(SEGMENT4)

SCHEMERUNNER = scheme.SchemeRunner(CONTROLLER.watercontroller(), SCHEME)

try:
    DISPLAY = display.InnerDisplay(THERMOMETERDHT)
    SCHEMERUNNER.start(True)
    CURRENT_SEGMENT = SCHEMERUNNER.current_segment

    while SCHEMERUNNER.status != scheme.RunnerStatus.Idle:
        if CURRENT_SEGMENT != SCHEMERUNNER.current_segment:
            CURRENT_SEGMENT = SCHEMERUNNER.current_segment
            print("Temperature: {}".format(THERMOMETER.temperature))
            print("Humidity: {}".format(THERMOMETERDHT.humidity))

except KeyboardInterrupt:
    pass
finally:
    print("stopping threads...")
    SCHEMERUNNER.stop()
    CONTROLLER.cleanup()
    print("done and closed")
