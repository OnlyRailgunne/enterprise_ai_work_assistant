import asyncio
import sys

from mcp import ClientSession
from mcp.client.stdio import (
    StdioServerParameters,
    stdio_client,
)


async def _send_email_via_mcp_async(
    draft_id: str,
):
    server_params = StdioServerParameters(
        command=sys.executable,
        args=["-m", "app.mcp.email_server"],
    )

    async with stdio_client(
        server_params
    ) as (read, write):

        async with ClientSession(
            read,
            write,
        ) as session:

            await session.initialize()

            result = await session.call_tool(
                "send_email",
                {
                    "draft_id": draft_id,
                },
            )

            return result


def send_email_via_mcp(
    draft_id: str,
):
    return asyncio.run(
        _send_email_via_mcp_async(
            draft_id
        )
    )