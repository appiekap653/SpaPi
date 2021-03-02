"""Segments for constructing water schemes"""

class WaterSegment:
    """Water segment to run water for a given duration"""
    def __init__(self, duration):
        self.on_time = duration

class IdleSegment:
    """Idle segment to wait for a given duration"""
    def __init__(self, duration):
        self.on_time = duration

class BurstSegment:
    """Burst segment to run water in burst for a given duration
    and a given delay and a number of times"""
    def __init__(self, on_time, off_time, burst_number):
        self.on_time = on_time
        self.off_time = off_time
        self.burst_number = burst_number
