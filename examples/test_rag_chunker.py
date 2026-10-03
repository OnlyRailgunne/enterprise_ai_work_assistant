from app.rag.loader import load_documents
from app.rag.chunker import chunk_document


documents = load_documents()

for document in documents:
    chunks = chunk_document(document["content"])

    print("=" * 60)
    print(document["filename"])
    print(f"Chunks: {len(chunks)}")

    for index, chunk in enumerate(chunks, start=1):
        print(f"\n--- Chunk {index} ---")
        print(chunk)