from app.crawlers.research_planner import plan_research

query = "Infosys vs TCS AI strategy"

data = plan_research(query)

print("\n==============================")
print("      RESEARCH REPORT")
print("==============================\n")

for angle, results in data.items():

    print(f"\n🔎 SEARCH ANGLE: {angle}")
    print("=" * 60)

    for i, result in enumerate(results, 1):

        print(f"\nResult #{i}")
        print("TITLE:", result.get("title"))
        print("URL:", result.get("url"))
        print("SNIPPET:", result.get("snippet"))

        content = result.get("page_content", "")

        print("\nEXTRACTED CONTENT:")
        print(content[:500])   
        print("\n" + "-"*60)
