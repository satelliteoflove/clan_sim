from game.models.character import Character
from game.models.item import Item
from game.models.skill import Skill

class Adventurer(Character):
    def __init__(self, name, race, alignment, stats, char_class):
        super().__init__(name, level=1, stats=stats)
        self.race = race
        self.alignment = alignment
        self.char_class = char_class
        self.experience = 0
        self.equipment = {}  # Equipment slots
        self.skills = []  # Skills

    def to_dict(self):
        data = super().to_dict()
        data.update({
            'race': self.race,
            'alignment': self.alignment,
            'char_class': self.char_class,
            'experience': self.experience,
            'equipment': {slot: item.to_dict() if item else None for slot, item in self.equipment.items()},
            'skills': [skill.to_dict() for skill in self.skills],
        })
        return data

    @classmethod
    def from_dict(cls, data):
        adventurer = cls(
            name=data['name'],
            race=data['race'],
            alignment=data['alignment'],
            stats=data['stats'],
            char_class=data['char_class']
        )
        adventurer.level = data['level']
        adventurer.experience = data['experience']
        adventurer.max_hp = data['max_hp']
        adventurer.current_hp = data['current_hp']
        adventurer.is_alive = data['is_alive']
        adventurer.is_defending = data.get('is_defending', False)
        # Reconstruct equipment
        adventurer.equipment = {}
        for slot, item_data in data['equipment'].items():
            if item_data:
                adventurer.equipment[slot] = Item.from_dict(item_data)
            else:
                adventurer.equipment[slot] = None
        # Reconstruct skills
        adventurer.skills = [Skill.from_dict(skill_data) for skill_data in data['skills']]
        return adventurer

