
import json

from groq import Groq

from app.agent.state import MultiAgentState


MODEL = "openai/gpt-oss-120b"

client = Groq()


def communication_agent(state: MultiAgentState):
    print()
    print("========== Communication Agent ==========")
    print()

    work_plan = state["work_plan"]

    messages = [
        {
            "role": "system",
            "content": """
You are a Communication Agent for an enterprise work assistant.

Your job is to turn an approved WorkPlan into an email draft.

Do not change the business decision in the WorkPlan.

Return JSON only:

{
    "recipients": ["E001"],
    "subject": "...",
    "content": "..."
}
""",
        },
        {
            "role": "user",
            "content": json.dumps(
                work_plan,
                ensure_ascii=False,
            ),
        },
    ]

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
    )

    content = response.choices[0].message.content
    email_draft = json.loads(content)

    print("Communication Agent final response:")
    print(
        json.dumps(
            email_draft,
            ensure_ascii=False,
            indent=4,
        )
    )

    return {
        "email_draft": email_draft
    }
