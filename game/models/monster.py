from game.models.character import Character

class Monster(Character):
    def __init__(self, name, level, stats, monster_type):
        super().__init__(name, level, stats)
        self.monster_type = monster_type
        # Additional monster-specific attributes

    def to_dict(self):
        data = super().to_dict()
        data.update({
            'monster_type': self.monster_type,
            # Include any additional attributes
        })
        return data

    @classmethod
    def from_dict(cls, data):
        monster = cls(
            name=data['name'],
            level=data['level'],
            stats=data['stats'],
            monster_type=data['monster_type']
        )
        monster.max_hp = data['max_hp']
        monster.current_hp = data['current_hp']
        monster.is_alive = data['is_alive']
        monster.is_defending = data.get('is_defending', False)
        # Initialize additional attributes if any
        return monster

