from voice_agent.planner import Planner


def test_planner_open_url():
    p = Planner()
    plan = p.plan("open https://example.com")
    assert plan.tool == "web.open_url"
    assert plan.args["url"].startswith("https://example.com")


def test_planner_search():
    p = Planner()
    plan = p.plan("search for python typing guide")
    assert plan.tool == "web.search_web"


def test_planner_create_file():
    p = Planner()
    plan = p.plan("create file tmp/test.txt")
    assert plan.tool == "code.create_file"
    assert plan.args["path"].endswith("tmp/test.txt")