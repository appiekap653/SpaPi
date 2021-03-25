"""Segments for constructing water schemes"""
import time
from abc import ABC, abstractmethod
from threading import Thread
from enum import Enum
from spapi import gpio_controller
from spapi.sauna import thermometer

class Segment(ABC):
    """
    The Segment interface declares operations common to all supported versions
    of the water segments.

    The SegmentsContext uses this interface to call the algorithm defined by Concrete
    Segments.
    """
    @abstractmethod
    def execute_segmemt(self, controller: gpio_controller.WaterController, runner) -> bool:
        """Method to execute the segment"""

    @property
    @abstractmethod
    def segment_type(self) -> str:
        """Returns a string representation of the segment type"""

    @property
    @abstractmethod
    def data(self) -> str:
        """Returns a string representation of comma-seperated segment data"""

class WaterSegment(Segment):
    """Water segment to run water for a given duration"""
    def __init__(self, duration: int):
        self._ontime = duration

    def execute_segmemt(self, controller: gpio_controller.WaterController, runner) -> bool:
        water_controller = controller

        t_end = time.time() + self._ontime

        while time.time() < t_end:
            water_controller.water_on()

            if not runner._start or runner._skip_backward or runner._skip_forward:
                break

        water_controller.water_off()

        return True

    @property
    def segment_type(self) -> str:
        return self.__class__.__name__

    @property
    def data(self) -> str:
        data = 'Duration:{}'.format(self._ontime)
        return data

    @property
    def duration(self) -> int:
        return self._ontime

    @duration.setter
    def duration(self, value: int):
        # Setting the duration
        self._ontime = value

class IdleSegment(Segment):
    """Idle segment to wait for a given duration"""
    def __init__(self, duration: int):
        self._ontime = duration

    def execute_segmemt(self, controller: gpio_controller.WaterController, runner) -> bool:
        water_controller = controller

        t_end = time.time() + self._ontime

        while time.time() < t_end:
            water_controller.water_off()

            if not runner._start or runner._skip_backward or runner._skip_forward:
                break

        return True

    @property
    def segment_type(self) -> str:
        return self.__class__.__name__

    @property
    def data(self) -> str:
        data = 'Duration:{}'.format(self._ontime)
        return data

    @property
    def duration(self) -> int:
        return self._ontime

    @duration.setter
    def duration(self, value: int):
        # Setting the duration
        self._ontime = value

class BurstSegment(Segment):
    """Burst segment to run water for a given duration then stop
    for a given duration and repeat for a specified number of times"""
    def __init__(self, duration_on: int, duration_off: int, repeat_number: int):
        self._ontime = duration_on
        self._offtime = duration_off
        self._repeatnumber = repeat_number

    def execute_segmemt(self, controller: gpio_controller.WaterController, runner) -> bool:
        water_controller = controller

        for _ in range(self._repeatnumber, 0, -1):
            t_on = time.time() + self._ontime

            while time.time() < t_on:
                water_controller.water_on()

                if not runner._start or runner._skip_backward or runner._skip_forward:
                    break

            t_off = time.time() + self._offtime

            while time.time() < t_off:
                water_controller.water_off()

                if not runner._start or runner._skip_backward or runner._skip_forward:
                    break

            if not runner._start or runner._skip_backward or runner._skip_forward:
                break

        return True

    @property
    def segment_type(self) -> str:
        return self.__class__.__name__

    @property
    def data(self) -> str:
        data = 'Duration_On:{},Duration_Off:{},Repeat_Number:{}'.format(self._ontime,
                                                                        self._offtime,
                                                                        self._repeatnumber)
        return data

    @property
    def duration_on(self) -> int:
        return self._ontime

    @duration_on.setter
    def duration_on(self, value: int):
        # Setting the duration
        self._ontime = value

    @property
    def duration_off(self) -> int:
        return self._offtime

    @duration_off.setter
    def duration_off(self, value: int):
        # Setting the duration
        self._offtime = value

    @property
    def repeat_number(self) -> int:
        return self._repeatnumber

    @repeat_number.setter
    def repeat_number(self, value: int):
        # Setting the duration
        self._repeatnumber = value

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


class RunnerStatus(Enum):
    """Representation of the current status of the SchemeRunner"""
    Idle = 0
    Running = 1
    Paused = 2


class SchemeRunner:
    """SchemeRunner to start/pause/resume a waterscheme"""

    def __init__(self, controller: gpio_controller.WaterController, scheme: WaterScheme):
        self._controller = controller
        self._waterscheme = scheme
        self._thread = Thread(target=self._thread_task)

        self._pause = False
        self._start = False
        self._repeat = False
        self._skip_forward = False
        self._skip_backward = False

        self._status = RunnerStatus.Idle
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
            self._thread.join()

    def start(self, repeat: bool = False):
        self._start = True
        self._status = RunnerStatus.Running
        self._repeat = repeat

        self._thread.start()

    def skip_forward(self) -> None:
        if self._start:
            self._skip_forward = True

    def skip_backward(self) -> None:
        if self._start:
            self._skip_backward = True

    def _thread_task(self):
        while self._start:
            i = 0
            while i < (len(self._waterscheme.segments)):
                segment = self._waterscheme.segments[i]

                while self._pause is True:
                    self._status = RunnerStatus.Paused
                self._status = RunnerStatus.Running

                temp = thermometer.read_temp()
                print('Temperature = {}'.format(temp))

                self._cur_segment_index = self._waterscheme.segments.index(segment)

                print('Executing Segment: {}'.format(segment.segment_type), flush=True)

                print('Segment Data: {}'.format(segment.data), flush=True)

                print('Current Index: {}'.format(self._waterscheme.segments.index(
                    self.current_segment)))

                print('Previous Index: {}'.format(self._waterscheme.segments.index(
                    self.previous_segment)))

                print('Next Index: {}'.format(self._waterscheme.segments.index(
                    self.next_segment)))

                segment.execute_segmemt(self._controller, self)

                self._prev_segment_index = self._waterscheme.segments.index(segment)

                if not self._start:
                    break

                if self._skip_backward:
                    i -= 1
                    self._skip_backward = False
                else:
                    self._skip_forward = False
                    i += 1

            if not self._repeat or not self._start:
                self._cur_segment_index = 0
                self._prev_segment_index = 0
                self._status = RunnerStatus.Idle
                self._start = False
                return

    @property
    def status(self) -> RunnerStatus:
        return self._status

    @property
    def current_segment(self) -> Segment:
        return self._waterscheme.segments[self._cur_segment_index]

    @property
    def next_segment(self) -> Segment:
        next_segment_index = self._cur_segment_index + 1

        if next_segment_index < len(self._waterscheme.segments):
            return self._waterscheme.segments[next_segment_index]

        return self._waterscheme.segments[0]

    @property
    def previous_segment(self) -> Segment:
        if self._prev_segment_index >= 0:
            return self._waterscheme.segments[self._prev_segment_index]

        return self._waterscheme.segments[0]

    @property
    def waterscheme(self) -> WaterScheme:
        # Getting the watherscheme
        return self._waterscheme

    @waterscheme.setter
    def waterscheme(self, value: WaterScheme):
        # Setting the watherscheme
        self._waterscheme = value
