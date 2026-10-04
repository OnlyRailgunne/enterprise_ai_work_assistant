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


create_task_schema = {
    "type": "function",
    "function": {
        "name": "create_task",
        "description": "Create a new work task.",
        "parameters": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "The task title.",
                },
                "description": {
                    "type": "string",
                    "description": "Detailed description of the task.",
                },
                "priority": {
                    "type": "string",
                    "enum": ["low", "medium", "high"],
                    "description": "Task priority.",
                },
                "employee_id": {
                    "type": ["string", "null"],
                    "description": (
                        "Employee ID such as E001. "
                        "Use null when the task has no assignee."
                    ),
                },
                "due_date": {
                    "type": "string",
                    "description": "Task due date in YYYY-MM-DD format.",
                },
            },
            "required": ["title"],
        },
    },
}


get_task_schema = {
    "type": "function",
    "function": {
        "name": "get_task",
        "description": "Get a work task by task ID.",
        "parameters": {
            "type": "object",
            "properties": {
                "task_id": {
                    "type": "string",
                    "description": "The UUID of the task.",
                },
            },
            "required": ["task_id"],
        },
    },
}


list_tasks_schema = {
    "type": "function",
    "function": {
        "name": "list_tasks",
        "description": (
            "List work tasks, optionally filtered by employee or status."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "employee_id": {
                    "type": ["string", "null"],
                    "description": (
                        "Employee ID such as E001. "
                        "Use null when no employee filter is needed."
                    ),
                },
                "status": {
                    "type": ["string", "null"],
                    "enum": [
                        "pending",
                        "in_progress",
                        "completed",
                        None,
                    ],
                    "description": (
                        "Filter tasks by status. "
                        "Use null when no status filter is needed."
                    ),
                },
            },
            "required": [],
        },
    },
}


update_task_schema = {
    "type": "function",
    "function": {
        "name": "update_task",
        "description": "Update an existing work task.",
        "parameters": {
            "type": "object",
            "properties": {
                "task_id": {
                    "type": "string",
                    "description": "The UUID of the task.",
                },
                "title": {
                    "type": ["string", "null"],
                    "description": "New task title.",
                },
                "description": {
                    "type": ["string", "null"],
                    "description": "New task description.",
                },
                "status": {
                    "type": ["string", "null"],
                    "enum": [
                        "pending",
                        "in_progress",
                        "completed",
                        None,
                    ],
                    "description": "New task status.",
                },
                "priority": {
                    "type": ["string", "null"],
                    "enum": [
                        "low",
                        "medium",
                        "high",
                        None,
                    ],
                    "description": "New task priority.",
                },
                "employee_id": {
                    "type": ["string", "null"],
                    "description": (
                        "New assignee employee ID such as E001. "
                        "Use null when the assignee should not be changed."
                    ),
                },
                "due_date": {
                    "type": ["string", "null"],
                    "description": "New task due date in YYYY-MM-DD format.",
                },
            },
            "required": ["task_id"],
        },
    },
}


complete_task_schema = {
    "type": "function",
    "function": {
        "name": "complete_task",
        "description": "Mark a work task as completed.",
        "parameters": {
            "type": "object",
            "properties": {
                "task_id": {
                    "type": "string",
                    "description": "The UUID of the task.",
                },
            },
            "required": ["task_id"],
        },
    },
}


create_event_schema = {
    "type": "function",
    "function": {
        "name": "create_event",
        "description": "Create a calendar event.",
        "parameters": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "Event title.",
                },
                "start_time": {
                    "type": "string",
                    "description": (
                        "Event start time in YYYY-MM-DD HH:MM:SS format."
                    ),
                },
                "end_time": {
                    "type": "string",
                    "description": (
                        "Event end time in YYYY-MM-DD HH:MM:SS format."
                    ),
                },
                "description": {
                    "type": ["string", "null"],
                    "description": "Event description.",
                },
                "location": {
                    "type": ["string", "null"],
                    "description": "Event location.",
                },
                "employee_id": {
                    "type": ["string", "null"],
                    "description": (
                        "Employee ID such as E001. "
                        "Use null when there is no organizer."
                    ),
                },
            },
            "required": [
                "title",
                "start_time",
                "end_time",
            ],
        },
    },
}


get_event_schema = {
    "type": "function",
    "function": {
        "name": "get_event",
        "description": "Get a calendar event by its ID.",
        "parameters": {
            "type": "object",
            "properties": {
                "event_id": {
                    "type": "string",
                    "description": "The UUID of the event.",
                },
            },
            "required": ["event_id"],
        },
    },
}


list_events_schema = {
    "type": "function",
    "function": {
        "name": "list_events",
        "description": (
            "List calendar events, optionally filtered by employee."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "employee_id": {
                    "type": ["string", "null"],
                    "description": (
                        "Employee ID such as E001. "
                        "Use null when no employee filter is needed."
                    ),
                },
            },
            "required": [],
        },
    },
}


cancel_event_schema = {
    "type": "function",
    "function": {
        "name": "cancel_event",
        "description": "Cancel a calendar event by its ID.",
        "parameters": {
            "type": "object",
            "properties": {
                "event_id": {
                    "type": "string",
                    "description": "The UUID of the event.",
                },
            },
            "required": ["event_id"],
        },
    },
}


create_email_draft_schema = {
    "type": "function",
    "function": {
        "name": "create_email_draft",
        "description": "Create an email draft for an employee.",
        "parameters": {
            "type": "object",
            "properties": {
                "employee_id": {
                    "type": "string",
                    "description": (
                        "Recipient employee ID such as E001."
                    ),
                },
                "subject": {
                    "type": "string",
                    "description": "Email subject.",
                },
                "body": {
                    "type": "string",
                    "description": "Email body.",
                },
            },
            "required": [
                "employee_id",
                "subject",
                "body",
            ],
        },
    },
}


get_email_draft_schema = {
    "type": "function",
    "function": {
        "name": "get_email_draft",
        "description": "Get an email draft by its ID.",
        "parameters": {
            "type": "object",
            "properties": {
                "draft_id": {
                    "type": "string",
                    "description": "The UUID of the email draft.",
                },
            },
            "required": ["draft_id"],
        },
    },
}


list_email_drafts_schema = {
    "type": "function",
    "function": {
        "name": "list_email_drafts",
        "description": (
            "List email drafts, optionally filtered by employee or status."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "employee_id": {
                    "type": ["string", "null"],
                    "description": (
                        "Recipient employee ID such as E001. "
                        "Use null when no employee filter is needed."
                    ),
                },
                "status": {
                    "type": ["string", "null"],
                    "enum": [
                        "draft",
                        "approved",
                        "sent",
                        None,
                    ],
                    "description": (
                        "Filter email drafts by status. "
                        "Use null when no status filter is needed."
                    ),
                },
            },
            "required": [],
        },
    },
}


update_email_draft_schema = {
    "type": "function",
    "function": {
        "name": "update_email_draft",
        "description": "Update an existing email draft.",
        "parameters": {
            "type": "object",
            "properties": {
                "draft_id": {
                    "type": "string",
                    "description": "The UUID of the email draft.",
                },
                "subject": {
                    "type": ["string", "null"],
                    "description": "New email subject.",
                },
                "body": {
                    "type": ["string", "null"],
                    "description": "New email body.",
                },
                "status": {
                    "type": ["string", "null"],
                    "enum": [
                        "draft",
                        "approved",
                        "sent",
                        None,
                    ],
                    "description": "New email draft status.",
                },
            },
            "required": ["draft_id"],
        },
    },
}


send_email_schema = {
    "type": "function",
    "function": {
        "name": "send_email",
        "description": (
            "Send an approved email draft."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "draft_id": {
                    "type": "string",
                    "description": "The UUID of the email draft.",
                },
            },
            "required": ["draft_id"],
        },
    },
}


approve_email_draft_schema = {
    "type": "function",
    "function": {
        "name": "approve_email_draft",
        "description": (
            "Approve an email draft so that it can be sent."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "draft_id": {
                    "type": "string",
                    "description": "The UUID of the email draft.",
                },
            },
            "required": ["draft_id"],
        },
    },
}

tool_schemas = [
    get_current_time_schema,
    search_employee_schema,
    search_enterprise_knowledge_schema,

    create_task_schema,
    get_task_schema,
    list_tasks_schema,
    update_task_schema,
    complete_task_schema,

    create_event_schema,
    get_event_schema,
    list_events_schema,
    cancel_event_schema,

    create_email_draft_schema,
    get_email_draft_schema,
    list_email_drafts_schema,
    update_email_draft_schema,
    send_email_schema,
    approve_email_draft_schema,
]