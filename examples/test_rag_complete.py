from langchain_core.messages import HumanMessage

from app.agent.graph import build_graph


graph = build_graph()


questions = [
    "How many days can employees work remotely?",
    "What is the employee salary policy?",
]


for question in questions:
    result = graph.invoke(
        {
            "messages": [
                HumanMessage(content=question)
            ]
        }
    )

    answer = result["messages"][-1].content

    print("=" * 60)
    print("Question:")
    print(question)

    print("\nAnswer:")
    print(answer)