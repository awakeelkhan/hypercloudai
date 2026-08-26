from skill import Skill
from search_tool import searchTool

filesystemSkill = Skill(
    name="filesystem",
    description="Tools for working with project files."
)
filesystemSkill.addTool(searchTool)