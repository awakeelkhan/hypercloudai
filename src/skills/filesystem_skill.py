from src.skills.skill import Skill

from src.tools.search_tool import searchTool
from src.tools.list_directory_tool import listDirectoryTool


filesystemSkill = Skill(
    name="filesystem",
    description="Tools for working with project files."
)

filesystemSkill.addTool(searchTool)
filesystemSkill.addTool(listDirectoryTool)