from app.rag.loader import load_documents


documents = load_documents()

print(f"Loaded {len(documents)} documents")

for document in documents:
    print("=" * 40)
    print(document["filename"])
    print(document["content"][:100])