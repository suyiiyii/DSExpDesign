
def test_route_planner():
    from app.route_planner import RoutePlanner,tm

    print(tm.dump())
    routers = RoutePlanner.get_all_paths(tm, "武汉", "广州")
    print(routers)