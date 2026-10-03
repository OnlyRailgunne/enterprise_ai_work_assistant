search_employee_schema = {
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
}


search_enterprise_knowledge_schema = {
    "type": "function",
    "function": {
        "name": "search_enterprise_knowledge",
        "description": (
            "Search the enterprise knowledge base for company policies, "
            "rules, procedures, and internal information."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The question or topic to search for.",
                },
            },
            "required": ["query"],
        },
    },
}


get_current_time_schema = {
    "type": "function",
    "function": {
        "name": "get_current_time",
        "description": "Get the current date and time.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    },
}


tool_schemas = [
    search_employee_schema,
    search_enterprise_knowledge_schema,
    get_current_time_schema,
]