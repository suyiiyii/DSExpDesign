import json

from models import City, Transport


def store(cities: list[City], transports: list[Transport]):
    with open("city.json", "w", encoding="utf-8") as f:
        f.write(json.dumps([city.__dict__ for city in cities]))
    with open("transport.json", "w", encoding="utf-8") as f:
        f.write(json.dumps([transport.__dict__ for transport in transports]))
    print("Data stored successfully")
    return


def generate_graph(transports: list[Transport]):
    with open("graph.md", "w", encoding="utf-8") as f:
        f.write("# 线路图\n")
        f.write("```mermaid\n")
        f.write("graph\n")
        '''深圳 -- G2944 --> 广州'''
        for transport in transports:
            f.write(f"\t{transport.start} -- {transport.run_id} --> {transport.end}\n")
        f.write("```")


def load() -> (list[City], list[Transport]):
    with open("city.json", "r", encoding="utf-8") as f:
        cities = [City(**city) for city in json.loads(f.read())]
    with open("transport.json", "r", encoding="utf-8") as f:
        transports = [Transport(**transport) for transport in json.loads(f.read())]
    generate_graph(transports)
    return cities, transports


if __name__ == '__main__':
    print(load())
