"""
SpaPi, Sauna and Automatic-Water control for RaspberryPi
"""
from water import controllers
from water import segments

CONTROLLER = controllers.WaterController(17)
SCHEME = segments.WaterScheme(CONTROLLER)

SEGMENT1 = segments.BurstSegment(3, 2, 2)
SEGMENT2 = segments.IdleSegment(480)
SEGMENT3 = segments.BurstSegment(5, 2, 4)
SEGMENT4 = segments.IdleSegment(300)

SCHEME.add(SEGMENT1)
SCHEME.add(SEGMENT2)
SCHEME.add(SEGMENT3)
SCHEME.add(SEGMENT4)

try:
    while True:
        print("running", flush=True)
        while not SCHEME.execute():   
            pass
except KeyboardInterrupt:
    pass
finally:
    CONTROLLER.cleanup()
    print("exiting...")
