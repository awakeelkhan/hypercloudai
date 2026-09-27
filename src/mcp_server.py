from mcp.server import MCPServer

mcp = MCPServer("HyperCloudTools")
@mcp.tool()
def getProjectInfo():
    return {
        "name": "HyperCloudAI",
        "description": "A small agentic framework",
        "purpose": "Learning how agent runtimes, tools and MCP work"
    }

if __name__ == "__main__":
    mcp.run()