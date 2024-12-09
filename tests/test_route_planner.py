
def test_route_planner():
    from app.route_planner import RoutePlanner,tm

    print(tm.dump())
    print(RoutePlanner.get_all_paths(tm, "深圳", "广州"))