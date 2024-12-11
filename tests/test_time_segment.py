from app.time_segment import TimeSegment


def test_create():
    ts = TimeSegment("06:00", "07:00")
    assert ts.start_time == "06:00"
    assert ts.end_time == "07:00"


def test_add():
    ts1 = TimeSegment("06:00", "07:00")
    ts2 = TimeSegment("07:00", "08:00")
    ts3 = ts1 + ts2
    assert ts3.start_time == "06:00"
    assert ts3.end_time == "08:00"
    assert ts3.total_time == 120


def test_add2():
    ts1 = TimeSegment("06:00", "07:00")
    ts2 = TimeSegment("07:30", "08:30")
    ts3 = ts1 + ts2
    assert ts3.start_time == "06:00"
    assert ts3.end_time == "08:30"
    assert ts3.total_time == 150


def test_add3():
    ts1 = TimeSegment("06:00", "07:00")
    ts2 = TimeSegment("01:30", "02:30")
    ts3 = ts1 + ts2
    assert ts3.start_time == "06:00"
    assert ts3.end_time == "02:30"
    assert ts3.total_time == 1230

def test_add4():
    ts1 = TimeSegment("06:00", "07:00")
    ts2 = TimeSegment("01:30", "06:30")
    ts3 = ts1 + ts2
    assert ts3.start_time == "06:00"
    assert ts3.end_time == "06:30"
    assert ts3.total_time == 1470
