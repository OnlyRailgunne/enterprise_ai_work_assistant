from app.db import save_document
from app.rag.loader import load_documents


documents = load_documents()

for document in documents:
    document_id = save_document(
        document["filename"],
        document["content"],
    )

    print(
        f"Saved: {document['filename']} "
        f"-> {document_id}"
    )