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

class WaterScheme:
    """Scheme that holds diferent segments to execute"""
    def __init__(self, watercontroller: controllers.WaterController):
        self.segments = []
        self.watercontroller = watercontroller

    def add(self, segment: Segment):
        self.segments.append(segment)

    def clear(self):
        self.segments.clear()

    def execute(self) -> bool:
        for segment in self.segments:
            print('Executing Segment {}'.format(segment), flush=True)
            temp = thermometer.read_temp()
            print('Temperature = {}'.format(temp))
            while not segment.execute_segmemt(self.watercontroller):
                pass
        return True
