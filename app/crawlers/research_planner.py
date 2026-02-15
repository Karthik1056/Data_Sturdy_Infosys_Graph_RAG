from app.crawlers.research_engine import dynamic_research


def plan_research(user_query: str):

    search_angles = [
        user_query,
        f"{user_query} partnerships",
        f"{user_query} AI strategy",
        # f"{user_query} investor relations",
        # f"{user_query} hiring trends"
    ]

    research_data = {}

    for angle in search_angles:
        research_data[angle] = dynamic_research(angle)

    return research_data
