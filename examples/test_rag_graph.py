from langchain_core.messages import HumanMessage

from app.agent.graph import build_graph


graph = build_graph()


query = "How many days can employees work remotely?"


result = graph.invoke(
    {
        "messages": [
            HumanMessage(content=query)
        ]
    }
)


print("Question:")
print(query)

print("\nAssistant Answer:")
print(result["messages"][-1].content)