"""Segments for constructing water schemes"""
import time
from abc import ABC, abstractmethod
from threading import Thread
from enum import Enum
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

    @property
    @abstractmethod
    def Type(self) -> str:
        """Returns a string representation of the segment type"""

    @property
    @abstractmethod
    def Data(self) -> str:
        """Returns a string representation of comma-seperated segment data"""

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

    @property
    def Type(self) -> str:
        return self.__class__.__name__

    @property
    def Data(self) -> str:
        data = 'Duration:{}'.format(self._ontime)
        return data

class IdleSegment(Segment):
    """Idle segment to wait for a given duration"""
    def __init__(self, duration):
        self._ontime = duration

    def execute_segmemt(self, watercontroller: controllers.WaterController) -> bool:
        t_end = time.time() + self._ontime

        while time.time() < t_end:
            watercontroller.water_off()
        return True

    @property
    def Type(self) -> str:
        return self.__class__.__name__

    @property
    def Data(self) -> str:
        data = 'Duration:{}'.format(self._ontime)
        return data

class BurstSegment(Segment):
    """Burst segment to run water for a given duration then stop 
    for a given duration and repeat for a specified number of times"""
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

    @property
    def Type(self) -> str:
        return self.__class__.__name__

    @property
    def Data(self) -> str:
        data = 'Duration_On:{},Duration_Off:{},Repeat_Number:{}'.format(self._ontime, self._offtime, self._repeatnumber)
        return data

class WaterScheme:
    """Scheme that holds diferent segments to execute"""
    def __init__(self):
        self._segments = []

    def __setitem__(self, pos: int, segment: Segment):
        if pos >= len(self._segments):
	        raise IndexError('list index out of range')
        self._segments[pos] = segment

    def __getitem__(self, pos: int):
        if pos >= len(self._segments):
            raise IndexError('list index out of range')
        return self._segments[pos]    

    def add(self, segment: Segment):
        self._segments.append(segment)

    def remove_at(self, pos: int):
        if pos >= len(self._segments):
            raise IndexError('list index out of range')
        del self._segments[pos]

    def clear(self):
        self._segments.clear()

    @property
    def segments(self) -> list:
        # Getting the segments
        return self._segments

"""Representation of the current status of the SchemeRunner"""
class RunnerStatus(Enum):
    Idle = 0
    Running = 1
    Paused = 2

"""SchemeRunner to start/pause/resume a waterscheme"""
class SchemeRunner:

    def __init__(self, controller: controllers.WaterController, scheme: WaterScheme):
        self._controller = controller
        self._waterscheme = scheme
        self._thread = Thread(target = self._thread_task)

        self._pause = False
        self._start = False
        self._repeat = False

        self._status = RunnerStatus.Idle
        self._current_segment = self._waterscheme[0]
        self._cur_segment_index = 0
        self._prev_segment_index = 0

    def pause(self) -> None:
        if self._start:
            self._pause = True

    def resume(self) -> None:
        self._pause = False

    def stop(self) -> None:
        if self._start:
            self._start = False
            self._thread._stop()
            self._thread.join()
        
    def start(self, repeat: bool = False):
        self._start = True
        self._status = RunnerStatus.Running
        self._repeat = repeat

        self._thread.start()

    def _thread_task(self):
        while self._start:
            for segment in self._waterscheme.segments:
                while self._pause is True:
                    self._status = RunnerStatus.Paused
                else:
                    self._status = RunnerStatus.Running

                temp = thermometer.read_temp()
                print('Temperature = {}'.format(temp))

                self._cur_segment_index = self._waterscheme.segments.index(segment)
                self._current_segment = segment

                print('Executing Segment: {}'.format(segment.Type), flush=True)
                print('Segment Data: {}'.format(segment.Data), flush=True)
                print('Current Index: {}'.format(self._waterscheme.segments.index(self.current_segment)))
                print('Previous Index: {}'.format(self._waterscheme.segments.index(self.previous_segment)))
                print('Next Index: {}'.format(self._waterscheme.segments.index(self.next_segment)))
                
                segment.execute_segmemt(self._controller)

                self._prev_segment_index = self._waterscheme.segments.index(segment)

                if not self._start:
                    break

            if not self._repeat or not self._start:
                self._cur_segment_index = 0
                self._prev_segment_index = 0
                self._current_segment = self._waterscheme[0]
                self._status = RunnerStatus.Idle
                self._start = False
                return
        
    @property
    def status(self) -> RunnerStatus:
        return self._status

    @property
    def current_segment(self) -> Segment:
        return self._current_segment

    @property
    def next_segment(self) -> Segment:
        if (self._cur_segment_index + 1) < len(self._waterscheme.segments):
            return self._waterscheme.segments[self._cur_segment_index + 1]
        else:
            return self._waterscheme.segments[0]

    @property
    def previous_segment(self) -> Segment:
        if self._prev_segment_index >= 0:
            return self._waterscheme.segments[self._prev_segment_index]
        else:
            return self._waterscheme.segments[0]

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
