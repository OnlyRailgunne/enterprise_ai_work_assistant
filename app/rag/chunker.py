def chunk_document(content):
    chunks = []

    paragraphs = content.split("\n\n")

    for paragraph in paragraphs:
        paragraph = paragraph.strip()

        if paragraph:
            chunks.append(paragraph)

    return chunks