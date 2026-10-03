from sentence_transformers import SentenceTransformer


model = SentenceTransformer("all-MiniLM-L6-v2")

text = "Employees may work remotely up to three days per week."

embedding = model.encode(text)

print("Embedding type:", type(embedding))
print("Embedding shape:", embedding.shape)
print("First 10 values:", embedding[:10])