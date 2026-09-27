from src.skills.skill_registry import SkillRegistry
from src.skills.filesystem_skill import filesystemSkill

def test_skill_registry():
    registry = SkillRegistry()
    registry.register(filesystemSkill)
    assert registry.get("filesystem") == filesystemSkill
    assert len(registry.getAll()) == 1