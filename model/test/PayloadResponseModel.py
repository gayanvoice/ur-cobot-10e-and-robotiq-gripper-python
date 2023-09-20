import json
from dataclasses import dataclass


@dataclass
class PayloadResponseModel:
    _status: bool
    _duration: float
    _start_perf_counter: float
    _end_perf_counter: float
    _message: str
