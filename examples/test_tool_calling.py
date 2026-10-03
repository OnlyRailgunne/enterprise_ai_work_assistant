from dotenv import load_dotenv
from groq import Groq

from app.tools import TOOLS


load_dotenv()


client = Groq()


tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "Get the current time in Tokyo.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_employee",
            "description": "Search for an employee by employee ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "employee_id": {
                        "type": "string",
                        "description": "The employee ID, such as E001.",
                    },
                },
                "required": ["employee_id"],
            },
        },
    },
]


messages = [
    {
        "role": "user",
        "content": "Tell me the information of employee E001.",
    }
]


# 第一次请求：让 LLM 判断是否需要 Tool
response = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=messages,
    tools=tools,
)

message = response.choices[0].message

print("Tool Calls:")
print(message.tool_calls)


if message.tool_calls:
    # 把 LLM 的 Tool Call 加入对话
    messages.append(message)

    for tool_call in message.tool_calls:
        tool_name = tool_call.function.name

        tool = TOOLS[tool_name]

        # Function Calling 的参数是 JSON 字符串
        import json

        arguments = json.loads(tool_call.function.arguments)

        result = tool(**arguments)

        print("\nTool Result:")
        print(result)

        # 把 Tool 执行结果加入对话
        messages.append(
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(result),
            }
        )


    # 第二次请求：让 LLM 根据 Tool Result 生成最终回答
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=messages,
        tools=tools,
    )

    final_message = response.choices[0].message

    print("\nFinal Answer:")
    print(final_message.content)