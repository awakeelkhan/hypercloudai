import os

from src.tools.tool import Tool


def searchProject(query):
    results = []

    for root, directories, files in os.walk("src"):
        directories[:] = [
            directory
            for directory in directories
            if directory != "__pycache__"
        ]

        for fileName in files:
            filePath = os.path.join(root, fileName)

            try:
                with open(
                    filePath,
                    "r",
                    encoding="utf-8"
                ) as file:
                    content = file.read()

                if query.lower() in content.lower():
                    results.append(filePath)

            except (UnicodeDecodeError, PermissionError):
                continue

    return results


searchTool = Tool(
    name="searchProject",
    description="Search the HyperCloudAI project files for a keyword.",
    inputSchema={
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The keyword to search for."
            }
        },
        "required": ["query"]
    },
    execute=searchProject
)