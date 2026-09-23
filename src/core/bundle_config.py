from src.core.agent_bundle import AgentBundle
from src.core.tool_permissions import ToolPermissions
from src.skills.skill_registry import SkillRegistry
from src.skills.filesystem_skill import filesystemSkill


def createAgentBundle(agent):
    registry = SkillRegistry()
    registry.register(filesystemSkill)

    tools = []

    for skill in registry.getAll():
        tools.extend(skill.getTools())

    permissions = ToolPermissions(
        allowedTools=["listDirectory", "searchProject"],
        deniedTools=[],
        readOnlyTools=["listDirectory", "searchProject"],
        actionTools=[]
    )

    return AgentBundle(
        agent,
        registry.getAll(),
        tools,
        ["src/mcp_server.py"],
        permissions
    )