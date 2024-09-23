class Monster:
    def __init__(self, name, stats, level):
        self.name = name
        self.stats = stats
        self.level = level
        self.max_hp = self.calculate_max_hp()
        self.current_hp = self.max_hp
        self.is_alive = True
    
    def calculate_max_hp(self):
        # Example formula for max HP
        return 5 + self.stats.get('Endurance', 5) * 2
