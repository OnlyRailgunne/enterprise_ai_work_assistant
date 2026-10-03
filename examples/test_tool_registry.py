from dotenv import load_dotenv

from app.tools import TOOLS


load_dotenv()


tool = TOOLS["search_employee"]

result = tool("E001")

print("Tool Result:")
print(result)