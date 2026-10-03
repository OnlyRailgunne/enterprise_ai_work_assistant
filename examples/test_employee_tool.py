from dotenv import load_dotenv

from app.tools.employee import search_employee


load_dotenv()


result = search_employee("E999")

print("Employee Result:")
print(result)