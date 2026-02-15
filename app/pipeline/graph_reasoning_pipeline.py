# from app.reasoning.intent_extractor import extract_intent
# from app.reasoning.graph_retriver import retrieve_graph_context
# from app.reasoning.answer_generator import generate_answer
# from app.reasoning.fallback_llm import fallback_summary


# def run_reasoning_pipeline(query: str):

#     print("\n🧠 Phase 3 — Strategic Reasoning Started...\n")

#     # STEP 1 — Extract intent
#     intent_data = extract_intent(query)

#     print("Intent:", intent_data)

#     # STEP 2 — Retrieve from Neo4j
#     context = retrieve_graph_context()

#     # ⭐ CRITICAL SAFETY CHECK
#     if not context or len(context) < 50:

#         print("⚠️ No graph relationships found.")
#         print("Switching to LLM fallback mode...\n")

#         fallback_answer = fallback_summary(query)

#         return {
#             "query": query,
#             "mode": "LLM_FALLBACK",
#             "answer": fallback_answer
#         }

#     # STEP 3 — Graph RAG Answer
#     answer = generate_answer(query, context)

#     return {
#         "query": query,
#         "mode": "GRAPH_RAG",
#         "answer": answer
#     }


from app.reasoning.intent_extractor import extract_intent
from app.reasoning.graph_retriver import retrieve_graph_context
from app.reasoning.answer_generator import generate_answer
from app.reasoning.fallback_llm import fallback_summary


def run_reasoning_pipeline(query: str):

    print("\n🧠 Phase 3 — Strategic Reasoning Started...\n")

    # STEP 1 — Extract intent
    intent_data = extract_intent(query)
    print("Intent:", intent_data)

    # STEP 2 — Safe Graph Retrieval
    try:
        context = retrieve_graph_context()
    except Exception as e:
        print("⚠️ Neo4j retrieval failed:", str(e))
        context = ""

    # STEP 3 — Evidence Count
    evidence_count = context.count("\n") if context else 0
    print(f"📊 Evidence triples found: {evidence_count}")

    # STEP 4 — Smart Routing
    if evidence_count < 5:

        print("⚠️ Weak graph signal. Switching to LLM fallback...\n")

        fallback_answer = fallback_summary(query)

        return {
            "query": query,
            "mode": "LLM_FALLBACK",
            "evidence_count": evidence_count,
            "answer": fallback_answer
        }

    # STEP 5 — GraphRAG Answer
    print("✅ Strong graph detected. Generating GraphRAG answer...\n")

    answer = generate_answer(query, context)

    return {
        "query": query,
        "mode": "GRAPH_RAG",
        "evidence_count": evidence_count,
        "answer": answer
    }
