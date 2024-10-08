class Skill:
    def __init__(self, name, level, effect):
        self.name = name
        self.level = level
        self.effect = effect

    def to_dict(self):
        return {
            'name': self.name,
            'level': self.level,
            'effect': self.effect,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data['name'],
            level=data['level'],
            effect=data['effect']
        )
