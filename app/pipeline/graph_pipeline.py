# from app.crawlers.research_planner import plan_research
# from app.extractors.triple_extractor import extract_triples
# from app.graph.graph_writer import write_triples_to_graph
# from app.utils.text_cleaner import clean_text
# from app.utils.text_chunker import chunk_text
# from app.db.source_writer import save_source


# from app.llm.triple_filter import filter_triples
# from app.llm.predicate_mapper import normalize_predicate


# def run_graph_pipeline(query: str):

#     print("\nPlanning research...\n")

#     research_data = plan_research(query)

#     total_triples = 0
#     seen_triples = set()   # ⭐ prevents duplicates

#     for angle, results in research_data.items():

#         print(f"\nResearch Angle → {angle}")

#         # for result in results:

#         #     content = result.get("page_content")

#         #     if not content or len(content) < 500:
#         #         continue

#         #     cleaned = clean_text(content)
#         #     chunks = chunk_text(cleaned)

#         #     for chunk in chunks:

#         #         raw_triples = extract_triples(chunk)

#         #         if not raw_triples:
#         #             continue

#         #         # ⭐ FILTER
#         #         triples = filter_triples(raw_triples)

#         #         normalized_triples = []

#         #         for t in triples:

#         #             t["predicate"] = normalize_predicate(t["predicate"])

#         #             triple_key = (
#         #                 t["subject"].lower(),
#         #                 t["predicate"].lower(),
#         #                 t["object"].lower()
#         #             )

#         #             # ⭐ DEDUP
#         #             if triple_key in seen_triples:
#         #                 continue

#         #             seen_triples.add(triple_key)
#         #             normalized_triples.append(t)

#         #         if normalized_triples:

#         #             write_triples_to_graph(normalized_triples)
#         #             total_triples += len(normalized_triples)



#     print(f"\nTOTAL HIGH QUALITY TRIPLES WRITTEN: {total_triples}")

#     return total_triples


from app.crawlers.research_planner import plan_research
from app.extractors.triple_extractor import extract_triples
from app.graph.graph_writer import write_triples_to_graph
from app.utils.text_cleaner import clean_text
from app.utils.text_chunker import chunk_text

from app.db.source_writer import save_crawled_source
from app.llm.triple_filter import filter_triples
from app.llm.predicate_mapper import normalize_predicate


def run_graph_pipeline(query: str):

    print("\n🔎 Planning research...\n")

    research_data = plan_research(query)

    total_triples = 0
    seen_triples = set()

    crawled_sources = []   # ⭐ STORE FOR JSON

    for angle, results in research_data.items():

        print(f"\n📚 Research Angle → {angle}")

        for result in results:

            title = result.get("title")
            url = result.get("url")
            content = result.get("page_content")

            if not content or len(content) < 500:
                continue


            # ⭐ ADD TO RESPONSE
            crawled_sources.append({
                "title": title,
                "url": url,
                "angle": angle,
                "content_length": len(content)
            })


            # optional DB save
            save_crawled_source(query, angle, title, url, content)


            cleaned = clean_text(content)
            chunks = chunk_text(cleaned)

            for chunk in chunks:

                raw_triples = extract_triples(chunk)

                if not raw_triples:
                    continue

                triples = filter_triples(raw_triples)

                normalized_triples = []

                for t in triples:

                    t["predicate"] = normalize_predicate(t["predicate"])

                    triple_key = (
                        t["subject"].lower(),
                        t["predicate"].lower(),
                        t["object"].lower()
                    )

                    if triple_key in seen_triples:
                        continue

                    seen_triples.add(triple_key)
                    normalized_triples.append(t)

                if normalized_triples:

                    write_triples_to_graph(normalized_triples)
                    total_triples += len(normalized_triples)

    print(f"\n✅ TOTAL HIGH QUALITY TRIPLES WRITTEN: {total_triples}\n")

    return {
        "query": query,
        "sources": crawled_sources,
        "triples_written": total_triples
    }

