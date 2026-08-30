from skill import Skill
from search_tool import searchTool
from list_directory_tool import listDirectoryTool

filesystemSkill = Skill(
    name="filesystem",
    description="Tools for working with project files."
)
filesystemSkill.addTool(searchTool)
filesystemSkill.addTool(listDirectoryTool)