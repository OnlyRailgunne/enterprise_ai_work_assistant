from app.db import save_chunk, save_document
from app.rag.chunker import chunk_document
from app.rag.embedder import embed_texts
from app.rag.loader import load_documents


documents = load_documents()

for document in documents:
    document_id = save_document(
        document["filename"],
        document["content"],
    )

    chunks = chunk_document(document["content"])

    texts = [chunk for chunk in chunks]

    embeddings = embed_texts(texts)

    for chunk, embedding in zip(chunks, embeddings):
        chunk_id = save_chunk(
            document_id,
            chunk,
            embedding,
        )

        print(
            f"Saved chunk: {chunk_id} "
            f"from {document['filename']}"
        )