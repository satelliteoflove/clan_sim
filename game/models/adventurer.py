# game/models/adventurer.py

class Adventurer:
    def __init__(self, name, race, alignment, stats, char_class):
        self.name = name
        self.race = race
        self.alignment = alignment
        self.stats = stats
        self.char_class = char_class
        self.level = 1
        self.experience = 0
        self.max_hp = self.calculate_max_hp()
        self.current_hp = self.max_hp
        self.is_alive = True
        self.equipment = {}
        self.skills = []
        self.is_defending = False

    def calculate_max_hp(self):
        return 10 + self.stats.get('Endurance', 5) * 2
