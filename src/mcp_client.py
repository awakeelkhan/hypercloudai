import anyio
from mcp import Client, StdioServerParameters

serverParams = StdioServerParameters(
    command="python",
    args=["src/mcp_server.py"]
)

async def main():
    async with Client(serverParams) as client:
        result = await client.list_tools()

        print("Available MCP Tools:")

        for tool in result.tools:
            print(tool.name)

        result = await client.call_tool("getProjectInfo", {})

        print("Tool Result:")
        print(result.content)
if __name__ == "__main__":
    anyio.run(main)