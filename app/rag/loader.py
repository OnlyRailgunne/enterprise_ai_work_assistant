from pathlib import Path


KNOWLEDGE_DIR = Path("knowledge")


def load_documents():
    documents = []

    for file_path in KNOWLEDGE_DIR.glob("*.md"):
        content = file_path.read_text(encoding="utf-8")

        documents.append(
            {
                "filename": file_path.name,
                "content": content,
            }
        )

    return documents