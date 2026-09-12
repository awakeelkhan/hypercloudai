import os

from src.tools.tool import Tool


def listDirectory():
    return os.listdir("src")


listDirectoryTool = Tool(
    name="listDirectory",
    description="List the files inside the src directory.",
    inputSchema={
        "type": "object",
        "properties": {}
    },
    execute=listDirectory
)