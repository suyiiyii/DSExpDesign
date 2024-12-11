from app.models import Transport
from app.store import db


def test_route_planner():
    from app.route_planner import RoutePlanner, tm, calc_total_cost

    print(tm.dump())
    routers = RoutePlanner.fastest_v2(tm, "上海", "厦门", "06:00")
    print(*routers,sep="\n")
    print(calc_total_cost(routers))


def test_fastest_version():
    from app.route_planner import RoutePlanner, tm, calc_total_cost
    cities = [x.name for x in db.cities]
    alg = [RoutePlanner.fastest_v2, RoutePlanner.fastest_v3]
    for city1 in cities:
        for city2 in cities:
            if city1 == city2:
                continue
            for start in ["06:00", "12:00", "18:00"]:
                result = []
                for a in alg:
                    path = a(tm, city1, city2, start)
                    result.append(path)
                    assert path[0].start == city1
                    assert path[-1].end == city2
                assert calc_total_cost(result[0], start)[1] == calc_total_cost(result[1], start)[1]


def test_transfer_least_version():
    from app.route_planner import RoutePlanner, tm
    cities = [x.name for x in db.cities]
    alg = [RoutePlanner.transfer_count_least_v2, RoutePlanner.transfer_count_least_v3]
    for city1 in cities:
        for city2 in cities:
            if city1 == city2:
                continue
            def count_transports(transports: list[Transport]) -> int:
                return len(set([x.run_id for x in transports]))

            result = []
            for a in alg:
                path = a(tm, city1, city2)
                result.append(path)
                assert path[0].start == city1
                assert path[-1].end == city2
            print(count_transports(result[0]) == count_transports(result[1]))
            for a in alg:
                path = a(tm, city1, city2)
                result.append(path)
            # assert count_transports(result[0]) == count_transports(result[1])
