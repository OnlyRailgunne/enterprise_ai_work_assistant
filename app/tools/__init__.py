from app.tools.employee import search_employee
from app.tools.knowledge import search_enterprise_knowledge
from app.tools.time import get_current_time


TOOLS = {
    "get_current_time": get_current_time,
    "search_employee": search_employee,
    "search_enterprise_knowledge": search_enterprise_knowledge,
}