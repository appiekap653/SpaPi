"""Segments for constructing water schemes"""
import time
from abc import ABC, abstractmethod
from threading import Thread
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
    then stop for a given duration and repeat a number of times"""
    def __init__(self, on_time, off_time, repeat_number: int):
        self._ontime = on_time
        self._offtime = off_time
        self._repeatnumber = repeat_number

    def execute_segmemt(self, watercontroller: controllers.WaterController) -> bool:
        for _ in range(self._repeatnumber, 0, -1):
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
        # Getting the segments
        return self._segments

"""SchemeRunner to start/pause/resume a waterscheme"""
class SchemeRunner:

    def __init__(self, controller: controllers.WaterController, scheme: WaterScheme):
        self._controller = controller
        self._waterscheme = scheme

        self._pause = False
        self._start = False
        self._repeat = False
        self._running = False

    def pause(self) -> None:
        self._pause = True

    def resume(self) -> None:
        self._pause = False

    def stop(self) -> None:
        self._start = False
        self._thread.join()
        self._running = False

    def start(self, repeat: bool):
        self._start = True
        self._running = True
        self._repeat = repeat

        self._thread = Thread(target = self._thread_task)
        self._thread.start()

    def _thread_task(self):
        while self._start:
            for segment in self._waterscheme.segments:
                while self._pause is True:
                    print("paused...")
                print('Executing Segment {}'.format(segment), flush=True)
                temp = thermometer.read_temp()
                print('Temperature = {}'.format(temp))
                segment.execute_segmemt(self._controller)

            if not self._repeat:
                self._running = False
                self._start = False
                return
        else:
            return

    @property
    def running(self) -> bool:
        return self._running

    @property
    def waterscheme(self) -> WaterScheme:
        # Getting the watherscheme
        return self._waterscheme

    @waterscheme.setter
    def waterscheme(self, value: WaterScheme):
        # Setting the watherscheme
        self._waterscheme=value

    @property
    def controller(self) -> controllers.WaterController:
        # Getting the Controller
        return self._controller

    @controller.setter
    def controller(self, value: controllers.WaterController):
        # Setting the controller
        self._controller=value
