import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END

from app.agent.state import AgentState
from app.db import search_chunks
from app.rag.embedder import embed_text


load_dotenv()


llm = ChatGroq(
    model="openai/gpt-oss-120b",
    api_key=os.getenv("GROQ_API_KEY"),
)


def agent_node(state: AgentState):
    messages = state["messages"]

    # 获取用户最新的问题
    user_message = messages[-1]

    query = user_message.content

    # 1. 将用户问题转换成 embedding
    query_embedding = embed_text(query)

    # 2. 从 PostgreSQL 检索相关企业知识
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

    # 4. 将企业知识加入 LLM Prompt
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

    return {
        "messages": [response]
    }


def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node(
        "agent",
        agent_node,
    )

    graph.add_edge(
        START,
        "agent",
    )

    graph.add_edge(
        "agent",
        END,
    )

    return graph.compile()