import time


class ResponseModel:
    def __init__(self):
        self._status = None
        self._duration = None
        self._start_perf_counter = time.perf_counter()
        self._end_perf_counter = None

    @property
    def status(self):
        return self._status

    @property
    def duration(self):
        return self._duration

    def get(self, status):
        self._end_perf_counter = time.perf_counter()
        self._status = status
        self._duration = self._end_perf_counter - self._start_perf_counter
        return self
