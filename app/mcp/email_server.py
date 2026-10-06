import asyncio

from mcp.server.mcpserver import MCPServer

from app.email_service import send_email_draft


server = MCPServer(
    name="enterprise-email-server",
    version="1.0.0",
)


@server.tool()
def send_email(
    draft_id: str,
) -> dict:
    """
    Send an approved email draft.

    The email draft must already be approved.
    """
    result = send_email_draft(draft_id)

    if result is None:
        return {
            "success": False,
            "message": "邮件不存在，或者邮件尚未审批通过。",
        }

    return {
        "success": True,
        "email": result,
    }


async def main():
    await server.run_stdio_async()


if __name__ == "__main__":
    asyncio.run(main())