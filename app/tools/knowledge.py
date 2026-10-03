from app.db import search_chunks
from app.rag.embedder import embed_text


def search_enterprise_knowledge(query):
    query_embedding = embed_text(query)

    results = search_chunks(
        query_embedding,
        limit=3,
    )

    if not results:
        return {
            "found": False,
            "results": [],
        }

    knowledge = []

    for filename, content, distance in results:
        knowledge.append(
            {
                "source": filename,
                "content": content,
            }
        )

    return {
        "found": True,
        "results": knowledge,
    }