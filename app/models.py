from dataclasses import dataclass


@dataclass
class City:
    name: str


@dataclass
class Transport:
    type: str
    name: str
    start: str
    end: str
    price: int
    start_time: str
    end_time: str
    run_id: str
