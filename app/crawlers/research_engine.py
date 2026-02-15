from app.crawlers.tools.search_tool import web_search
from app.crawlers.tools.content_extractor import extract_webpage_content


def dynamic_research(query: str):

    search_results = web_search(query)

    intelligence_bundle = []

    for result in search_results:

        page_content = extract_webpage_content(result["url"])

        intelligence_bundle.append({
            "title": result["title"],
            "url": result["url"],
            "snippet": result["snippet"],
            "page_content": page_content
        })

    return intelligence_bundle
