from app.db import search_chunks
from app.rag.embedder import embed_text


query = "How many days can employees work remotely?"

query_embedding = embed_text(query)

results = search_chunks(query_embedding, limit=3)

print("Query:", query)
print()

for index, (filename, content, distance) in enumerate(
    results,
    start=1,
):
    print("=" * 60)
    print(f"Result {index}")
    print("Filename:", filename)
    print("Distance:", distance)
    print("Content:", content)