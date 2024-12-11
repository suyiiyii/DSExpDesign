DAY = 60 * 24


class TimeSegment:
    """时间片段类，用于计算时间差，实现时间段的加法"""

    @staticmethod
    def time2int(time_str: str | int) -> int:
        '''将时间字符串转换为整数'''
        if isinstance(time_str, int):
            return time_str
        h, m = map(int, time_str.split(':'))
        return h * 60 + m

    @staticmethod
    def int2time(time_int: int | str) -> str:
        '''将整数转换为时间字符串'''
        if isinstance(time_int, str):
            return time_int
        h, m = divmod(time_int, 60)
        return f"{h:02d}:{m:02d}"

    @staticmethod
    def time_delta(t_from: str | int, t_to: str | int) -> int:
        '''计算两个时间字符串的时间差，如果t_from > t_to，则认为是第二天的时间'''
        if isinstance(t_from, str):
            t_from = TimeSegment.time2int(t_from)
        if isinstance(t_to, str):
            t_to = TimeSegment.time2int(t_to)

        if t_from <= t_to:
            return t_to - t_from
        else:
            return DAY - t_from + t_to

    def __init__(self, start_time: int | str, end_time: int | str, total_time: int = 0):
        self.start_time_int: int = TimeSegment.time2int(start_time)
        self.end_time_int: int = TimeSegment.time2int(end_time)
        if total_time:
            self.total_time = total_time
        else:
            self.total_time = TimeSegment.time_delta(start_time, end_time)

    @property
    def start_time(self) -> str:
        return TimeSegment.int2time(self.start_time_int)

    @property
    def end_time(self) -> str:
        return TimeSegment.int2time(self.end_time_int)

    def __str__(self):
        return f"{self.start_time_int} - {self.end_time_int} ({self.total_time} min)"

    def __add__(self, other: "TimeSegment") -> "TimeSegment":
        """时间段的相加，会自动加上两个之间段之间的空隙"""
        return TimeSegment(self.start_time_int,
                           other.end_time_int,
                           self.total_time + TimeSegment.time_delta(self.end_time_int,
                                                                    other.start_time_int) + other.total_time)

    def __lt__(self, other):
        return self.total_time < other.total_time
