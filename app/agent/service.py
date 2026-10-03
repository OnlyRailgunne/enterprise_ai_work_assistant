from app.agent.graph import build_graph

graph = build_graph()


def run_agent(messages):
    result = graph.invoke(
        {"messages": messages}
    )

    return result


def stream_agent(messages):
    for chunk in graph.stream(
        {"messages": messages},
        stream_mode="messages",
    ):
        message_chunk, metadata = chunk

        if message_chunk.content:
            yield message_chunk.content