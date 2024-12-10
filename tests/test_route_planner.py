
def test_route_planner():
    from app.route_planner import RoutePlanner,tm

    print(tm.dump())
    routers = RoutePlanner.fastest_v2(tm, "上海", "厦门")
    print(routers)