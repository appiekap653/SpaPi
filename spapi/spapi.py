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

SEGMENT1 = segments.BurstSegment(3, 3, 2)
SEGMENT2 = segments.IdleSegment(60)
SEGMENT3 = segments.BurstSegment(3, 3, 2)
SEGMENT4 = segments.IdleSegment(60)
SEGMENT5 = segments.BurstSegment(3, 3, 2)
SEGMENT6 = segments.IdleSegment(60)

SCHEME.add(SEGMENT1)
SCHEME.add(SEGMENT2)
SCHEME.add(SEGMENT3)
SCHEME.add(SEGMENT4)
SCHEME.add(SEGMENT5)
SCHEME.add(SEGMENT6)

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
