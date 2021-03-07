"""Segments for constructing water schemes"""
import time
from abc import ABC, abstractmethod
from water import controllers
from sauna import thermometer

class Segment(ABC):
    """
    The Segment interface declares operations common to all supported versions
    of the water segments.

    The SegmentsContext uses this interface to call the algorithm defined by Concrete
    Segments.
    """
    @abstractmethod
    def execute_segmemt(self, watercontroller: controllers.WaterController) -> bool:
        """Method to execute the segment"""

class WaterSegment(Segment):
    """Water segment to run water for a given duration"""
    def __init__(self, duration):
        self._ontime = duration

    def execute_segmemt(self, watercontroller: controllers.WaterController) -> bool:
        t_end = time.time() + self._ontime

        while time.time() < t_end:
            watercontroller.water_on()
        watercontroller.water_off()
        return True

class IdleSegment(Segment):
    """Idle segment to wait for a given duration"""
    def __init__(self, duration):
        self._ontime = duration

    def execute_segmemt(self, watercontroller: controllers.WaterController) -> bool:
        t_end = time.time() + self._ontime

        while time.time() < t_end:
            watercontroller.water_off()
        return True

class BurstSegment(Segment):
    """Burst segment to run water in burst for a given duration
    and a given delay and a number of times"""
    def __init__(self, on_time, off_time, burst_number):
        self._ontime = on_time
        self._offtime = off_time
        self._burstnumber = burst_number

    def execute_segmemt(self, watercontroller: controllers.WaterController) -> bool:
        for _ in range(self._burstnumber, 0, -1):
            t_on = time.time() + self._ontime
            while time.time() < t_on:
                watercontroller.water_on()
            t_off = time.time() + self._offtime
            while time.time() < t_off:
                watercontroller.water_off()
        return True

"""Scheme that holds diferent segments to execute"""
class WaterScheme:

    def __init__(self):
        self._segments = []

    def __setitem__(self, pos, segment: Segment):
        self._segments[pos] = segment

    def __getitem__(self, pos):
        return self._segments[pos]

    def add(self, segment: Segment):
        self._segments.append(segment)

    def remove_at(self, pos):
        del self._segments[pos]

    def clear(self):
        self._segments.clear()

    @property
    def segments(self):
        return self._segments

"""SchemeRunner to start/pause/resume a waterscheme"""
class SchemeRunner:

    def __init__(self, controller: controllers.WaterController, scheme: WaterScheme):
        self._controller = controller
        self._waterscheme = scheme

        self._pause = False
        self._start = False

    def pause(self) -> None:
        self._pause = True

    def resume(self) -> None:
        self._pause = False

    def stop(self) -> None:
        self._start = False

    def start(self, repeat: bool):
        self._start = True

        while self._start:
            for segment in self._waterscheme.segments:
                while self._pause is True:
                    print("paused...")
                print('Executing Segment {}'.format(segment), flush=True)
                temp = thermometer.read_temp()
                print('Temperature = {}'.format(temp))
                segment.execute_segmemt(self._controller)

            if not repeat:
                return
        else:
            return

    @property
    def waterscheme(self):
        # Getting the watherscheme
        return self._waterscheme

    @waterscheme.setter
    def waterscheme(self, value):
        # setting the watherscheme
        self._waterscheme=value

    @property
    def controller(self):
        # Getting the Controller
        return self._controller

    @controller.setter
    def controller(self, value):
        # When the rows are changed, the columns are updated
        self._controller=value
