from app.tools.employee import search_employee
from app.tools.knowledge import search_enterprise_knowledge
from app.tools.time import get_current_time

from app.tools.task import (
    create_task,
    get_task,
    list_tasks,
    update_task,
    complete_task,
)

from app.tools.event import (
    create_event,
    get_event,
    list_events,
    cancel_event,
)

from app.tools.email import (
    create_email_draft,
    get_email_draft,
    list_email_drafts,
    update_email_draft,
    send_email,
    approve_email_draft,
)


TOOLS = {
    "get_current_time": get_current_time,
    "search_employee": search_employee,
    "search_enterprise_knowledge": search_enterprise_knowledge,

    "create_task": create_task,
    "get_task": get_task,
    "list_tasks": list_tasks,
    "update_task": update_task,
    "complete_task": complete_task,

    "create_event": create_event,
    "get_event": get_event,
    "list_events": list_events,
    "cancel_event": cancel_event,

    "create_email_draft": create_email_draft,
    "get_email_draft": get_email_draft,
    "list_email_drafts": list_email_drafts,
    "update_email_draft": update_email_draft,
    "send_email": send_email,
    "approve_email_draft": approve_email_draft,
}