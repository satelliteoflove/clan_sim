# game/models/character.py

class Character:
    def __init__(self, name, level, stats):
        self.name = name
        self.level = level
        self.stats = stats
        self.max_hp = self.calculate_max_hp()
        self.current_hp = self.max_hp
        self.is_alive = True
        self.is_defending = False

    def calculate_max_hp(self):
        # Example (crappy) formula for max HP
        return 10 + self.stats.get('Endurance', 5) * 2

    def take_damage(self, damage):
        self.current_hp -= damage
        if self.current_hp <= 0:
            # Prevent negative HP and mark as dead
            self.current_hp = 0
            self.is_alive = False 

    def attack(self, target):
        damage = self.calculate_damage(target)
        target.take_damage(damage)
        return damage

    def calculate_damage(self, target):
        # Simple damage formula: attacker's Strength minus target's Endurance
        base_damage = self.stats.get('Strength', 5) - target.stats.get('Endurance', 5)
        if base_damage < 1:
            base_damage = 1
        if target.is_defending:
            base_damage = base_damage // 2  # Defender takes half damage
            # TODO: Reset defending status at end of turn
        return base_damage

    def to_dict(self):
        return {
            'name': self.name,
            'level': self.level,
            'stats': self.stats,
            'max_hp': self.max_hp,
            'current_hp': self.current_hp,
            'is_alive': self.is_alive,
            'is_defending': self.is_defending,
        }

    @classmethod
    def from_dict(cls, data):
        character = cls(
            name=data['name'],
            level=data['level'],
            stats=data['stats']
        )
        character.max_hp = data['max_hp']
        character.current_hp = data['current_hp']
        character.is_alive = data['is_alive']
        character.is_defending = data.get('is_defending', False)
        return character

