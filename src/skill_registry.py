class SkillRegistry:
    def __init__(self):
        self.skills = []

    def register(self, skill):
        self.skills.append(skill)

    def get(self, name):
        for skill in self.skills:
            if skill.name == name:
                return skill
        return None

    def getAll(self):
        return self.skills