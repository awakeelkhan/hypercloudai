from src.skills.filesystem_skill import filesystemSkill

def test_filesystem_skill():
    assert filesystemSkill.name == "filesystem"
    assert len(filesystemSkill.getTools()) == 2