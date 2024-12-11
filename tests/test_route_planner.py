def test_route_planner():
    from app.route_planner import RoutePlanner, tm, calc_total_cost

    print(tm.dump())
    routers = RoutePlanner.fastest_v2(tm, "上海", "厦门", "06:00")
    print(*routers,sep="\n")
    print(calc_total_cost(routers))
