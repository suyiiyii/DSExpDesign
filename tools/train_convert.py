import json
from pathlib import Path

import httpx

BASE_DIR = Path(__file__).resolve().parent
STATION_NAME_PATH = BASE_DIR / 'station_name.txt'
SAMPLE_PATH = BASE_DIR / 'sample.txt'
TRAIN_NAME_PATH = BASE_DIR / 'train_name.txt'
DONE_STORE_PATH = BASE_DIR / 'done.json'


import sys
sys.path.append(str(BASE_DIR.parent))
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


with open(STATION_NAME_PATH, 'r', encoding="utf-8") as f:
    for line in f:
        parse_line(line)


def parse_copy_data(data: str) -> list[dict[str, str | float]]:
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
            data['price'] = 0.0
        return data

    parsed_train_info = []
    for line in data.strip().split('\n'):
        train_info = parse_data_line(line)
        if train_info:
            parsed_train_info.append(train_info)
    return parsed_train_info


class DoneStore:


    def __init__(self):
        self._data: list[str] = []
        self._load()

    def _load(self):
        with open(DONE_STORE_PATH, 'r', encoding='utf-8') as f:
            self._data = json.loads(f.read())

    def _store(self):
        with open(DONE_STORE_PATH, 'w', encoding='utf-8') as f:
            f.write(json.dumps(self._data))

    def add(self, train_name: str):
        self._data.append(train_name)
        self._store()

    def check(self, train_name: str):
        return train_name in self._data


done_store = DoneStore()
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
    if result and result[-1].end == "":
        del result[-1]
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


def check_if_exists(train_name) -> bool:
    for t in db.transports:
        if t.run_id == train_name:
            return True

def add_data(transports: list[Transport]):
    for transport in transports:
        db.add_transport(transport)


def parse_table_data(rows: list[list[str]]) -> list[dict[str, str | float]]:
    """解析表格数据"""
    datas = []
    for row in rows:
        data = {}
        data['start_station'] = row[1].strip()
        data['arrive_time'] = row[2].strip()
        data['start_time'] = row[4].strip()
        try:
            data['price'] = float(row[8].split('/')[0].strip())
        except ValueError:
            data['price'] = 0.0
        datas.append(data)
    return datas


def download_train_data(train_name: str) -> list[list[str]]:
    from bs4 import BeautifulSoup
    url = f"https://shike.gaotie.cn/checi.asp?checi={train_name.strip()}"
    response = httpx.get(url)
    if response.status_code != 200:
        raise RuntimeError(f"请求失败，状态码：{response.status_code}")

    soup = BeautifulSoup(response.text, 'lxml')
    table = soup.select_one('body > div:nth-child(2) > table:nth-child(5)')

    # Extract rows
    rows = []
    for row in table.find_all('tr')[1:]:  # Skip the header row
        cells = row.find_all('td')
        rows.append([cell.text for cell in cells])

    return rows


def download_and_save_train_data(train_name: str):
    if done_store.check(train_name) or check_if_exists(train_name):
        print(f"车次 {train_name} 已经存在，跳过获取")
        return
    print(f"开始获取车次 {train_name} 的数据")
    rows = download_train_data(train_name)
    datas = parse_table_data(rows)
    transports = calc_result(train_name, datas)
    add_data(transports)
    from time import sleep
    sleep_time = 10
    print(f"车次 {train_name} 的数据获取完成，成功获取 {len(transports)} 条数据，等待 {sleep_time} 秒")
    done_store.add(train_name)
    sleep(sleep_time)


if __name__ == '__main__':
    with open(TRAIN_NAME_PATH, 'r', encoding="utf-8") as f:
        for line in f:
            if line.strip():
                if "#" in line:
                    continue
                download_and_save_train_data(line.strip())
