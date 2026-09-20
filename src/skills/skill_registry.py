class SkillRegistry:
    def __init__(self):
        self.skills = {}

    def register(self, skill):
        self.skills[skill.name] = skill

    def get(self, skillName):
        return self.skills.get(skillName)

    def getAll(self):
        return list(self.skills.values())