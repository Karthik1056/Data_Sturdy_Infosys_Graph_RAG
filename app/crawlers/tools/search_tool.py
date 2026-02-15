from tavily import TavilyClient
from app.config import TAVILY_API_KEY

client = TavilyClient(api_key=TAVILY_API_KEY)


def web_search(query: str, max_results: int = 3):

    response = client.search(
        query=query,
        search_depth="basic",
        max_results=max_results
    )

    results = []

    for r in response["results"]:
        results.append({
            "title": r["title"],
            "url": r["url"],
            "snippet": r["content"]
        })

    return results
