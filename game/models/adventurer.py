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
        self.equipment = {}
        self.skills = []
        # Additional initialization as needed

