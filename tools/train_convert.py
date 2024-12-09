import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
TRAIN_NAME_PATH = BASE_DIR / 'station_name.txt'
SAMPLE_PATH = BASE_DIR / 'sample.txt'

station_name_dict = {}

from app.store import db
from app.models import Transport

cities = [x.name for x in db.cities]


def parse_line(line: str):
    """解析车站名"""
    line = line.strip()
    if not line:
        return
    splits = line.split('|')
    station_name_dict[splits[1]] = splits[-1]


with open(TRAIN_NAME_PATH, 'r', encoding="utf-8") as f:
    for line in f:
        parse_line(line)


def parse_data(data: str):
    """解析从网站上面复制下来的车站数据 来源网站：https://shike.gaotie.cn/checi.asp?checi=G305"""

    def parse_data_line(line: str) -> dict[str, str | float]:
        line = line.strip()
        if not line:
            return {}
        splits = line.split('\t')
        data = {}
        data['start_station'] = splits[1].strip()
        data['arrive_time'] = splits[2].strip()
        data['start_time'] = splits[4].strip()
        try:
            data['price'] = float(splits[8].split('/')[0].strip())
        except ValueError:
            data['price'] = 0
        return data

    datas = []
    for line in data.split('\n'):
        data = parse_data_line(line)
        if data:
            datas.append(data)
    return datas


def calc_result(train_name: str, datas: list[dict[str, str | int]]) -> list[Transport]:
    """计算车站之间的数据，得到可用的结果"""
    result: list[Transport] = []
    last_data = None
    for idx, data in enumerate(datas):
        station_name = data['start_station'].replace('站', '')
        if not (station_name in station_name_dict and station_name_dict[station_name] in cities):
            # 如果车站所处的城市不在目标城市中，则跳过
            continue

        if result:
            if station_name_dict[station_name] == result[-1].start:
                last_data = data
                continue
            # 如果当前车站和前一个车站不在同一个城市
            # 则将当前车站的信息添加到上一条信息中
            result[-1].end = station_name_dict[station_name]
            result[-1].end_time = data['arrive_time']
            result[-1].price = int(data['price'] - last_data['price'])
        if idx == len(datas) - 1:
            # 如果是最后一个车站，就不需要添加信息了
            break
        # 创建当前车站的信息
        transport = Transport(
            type='train',
            name=train_name,
            start=station_name_dict[station_name],
            end="",
            price=-1,
            start_time=data['start_time'],
            end_time="",
            run_id=train_name
        )
        result.append(transport)
        last_data = data
    return result


def to_dict(transport: Transport) -> dict:
    return {
        "type": transport.type,
        "name": transport.name,
        "start": transport.start,
        "end": transport.end,
        "price": transport.price,
        "start_time": transport.start_time,
        "end_time": transport.end_time,
        "run_id": transport.run_id
    }


if __name__ == '__main__':
    # with open(SAMPLE_PATH, 'r', encoding="utf-8") as f:
    #     data = f.read()
    #     datas = parse_data(data)
    # print(station_name_dict)
    # print(datas)
    train_name = input("请输入车次:")
    raw_data = ""
    raw_data += input("请输入数据:")
    while True:
        line = input()
        if not line:
            break
        raw_data += '\n' + line
    datas = parse_data(raw_data)
    print(json.dumps(list(map(to_dict, calc_result(train_name, datas))), ensure_ascii=False, indent=2))
