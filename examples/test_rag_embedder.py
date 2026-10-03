from app.rag.loader import load_documents
from app.rag.chunker import chunk_document
from app.rag.embedder import embed_texts


documents = load_documents()

all_chunks = []

for document in documents:
    chunks = chunk_document(document["content"])

    for chunk in chunks:
        all_chunks.append(
            {
                "filename": document["filename"],
                "content": chunk,
            }
        )


texts = [chunk["content"] for chunk in all_chunks]

embeddings = embed_texts(texts)

print("Total chunks:", len(all_chunks))
print("Embedding shape:", embeddings.shape)

for index in range(3):
    print("=" * 60)
    print("Filename:", all_chunks[index]["filename"])
    print("Content:", all_chunks[index]["content"])
    print("Vector shape:", embeddings[index].shape)