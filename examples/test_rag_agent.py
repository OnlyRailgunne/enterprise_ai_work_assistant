import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq

from app.db import search_chunks
from app.rag.embedder import embed_text


load_dotenv()


llm = ChatGroq(
    model="openai/gpt-oss-120b",
    api_key=os.getenv("GROQ_API_KEY"),
)


query = "How many days can employees work remotely?"


# 1. 将用户问题转换成 embedding
query_embedding = embed_text(query)


# 2. 从 PostgreSQL 检索相关知识
results = search_chunks(
    query_embedding,
    limit=3,
)


# 3. 将检索结果组成 Context
context_parts = []

for filename, content, distance in results:
    context_parts.append(
        f"Source: {filename}\n"
        f"Content: {content}"
    )


context = "\n\n".join(context_parts)


# 4. 将问题 + 企业知识交给 LLM
prompt = f"""
You are an enterprise AI assistant.

Answer the user's question using the provided enterprise knowledge.

Enterprise knowledge:
{context}

User question:
{query}

If the answer is not available in the enterprise knowledge,
say that the information is not available.
"""


# 5. 调用 LLM
response = llm.invoke(prompt)


print("Question:")
print(query)

print("\nRetrieved Knowledge:")
print(context)

print("\nAssistant Answer:")
print(response.content)