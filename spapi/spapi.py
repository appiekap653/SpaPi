"""
import sys
import os

module_path = os.path.abspath(os.getcwd())

if module_path not in sys.path:

    sys.path.append(module_path)
"""
from components.water import controllers
from components.water import segments

CONTROLLER = controllers.WaterController(17)
SCHEME = segments.WaterScheme(CONTROLLER)

SEGMENT1 = segments.BurstSegment(3, 2, 2)
SEGMENT2 = segments.IdleSegment(300)
SEGMENT3 = segments.BurstSegment(5, 2, 4)
SEGMENT4 = segments.IdleSegment(120)

SCHEME.add(SEGMENT1)
SCHEME.add(SEGMENT2)
SCHEME.add(SEGMENT3)
SCHEME.add(SEGMENT4)

try:
    while True:
        while not SCHEME.execute():
            print("running")

except KeyboardInterrupt:
    CONTROLLER.cleanup()
    print("exiting...")
finally:
    CONTROLLER.cleanup()
    print("exiting...")
