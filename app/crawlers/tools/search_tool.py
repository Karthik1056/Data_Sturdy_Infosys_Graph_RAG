from tavily import TavilyClient
from app.config import TAVILY_API_KEY

client = TavilyClient(api_key=TAVILY_API_KEY)


def web_search(query: str):
    """
    Tavily API Limits:
    - Free tier: 1000 requests/month
    - Basic plan: search_depth="basic" (faster, less comprehensive)
    - Advanced plan: search_depth="advanced" (slower, more comprehensive)
    - max_results: typically 5-10 for free tier
    """
    
    response = client.search(
        query=query,
        search_depth="basic", 
        include_raw_content=True,  # Get full page content
        include_images=False  # Skip images to save quota
    )

    results = []

    for r in response.get("results", []):
        results.append({
            "title": r.get("title", ""),
            "url": r.get("url", ""),
            "snippet": r.get("content", ""),
            "raw_content": r.get("raw_content", "")  # Full page content
        })

    return results
