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
        self.equipment = {
            'primary_hand': None,
            'secondary_hand': None,
            'head': None,
            'body': None,
            'accessory': None
        }
        self.skills = []  # Skills

    def equip_item(self, item):
        if not item.is_compatible(self):
            print(f"\n{self.name} cannot equip {item.name} due to class or alignment restrictions.")
            return False
        slot = item.slot
        if slot not in self.equipment:
            print(f"\n{slot} is not a valid equipment slot for {self.name}.")
            return False
        # Unequip current item in the slot, if any
        if self.equipment[slot]:
            self.unequip_item(slot)
        # Equip the new item
        self.equipment[slot] = item
        # TODO: move this to a new function
        for stat, value in item.attributes.items():
            self.stats[stat] = self.stats.get(stat, 0) + value

    def unequip_item(self, slot):
        if self.equipment.get(slot):
            item = self.equipment[slot]
            # TODO: move this to a new function
            for stat, value in item.attributes.items():
                self.stats[stat] = self.stats.get(stat, 0) - value
            self.equipment[slot] = None
            return item
        else:
            print(f"\nNo item equiopped in the {slot} slot.")
            return None

    # TODO: Implement the following
    # Please make the following adjustments and give me the new code as a regular code block (no diff notation):
    # game/models/adventurer.py:
    # I really don't like that way of managing item statistic adjustments, specifically because it is calculated by the equip_item() and unequip_item() functions and thus only calculated when those run. Let's break that out into a function that will re-calculate all stat adjustments for all equipped items whenever called.

    def print_equipment(self):
        print("\nCurrent Equipment:")
        for slot, item in self.equipment.items():
            item_name = item.name if item else '[Empty]'
            print(f"{slot.capitalize()}: {item_name}")

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
        adventurer.equipment = {
            'primary_hand': None,
            'secondary_hand': None,
            'head': None,
            'body': None,
            'accessory': None
        }
        for slot, item_data in data['equipment'].items():
            if item_data:
                item = Item.from_dict(item_data)
                adventurer.equipment[slot] = item
                # Apply item attributes to stats (this functionality will
                # be updated to be more flexible in the future)
                for stat, value in item.attributes.items():
                    adventurer.stats[stat] = adventurer.stats.get(stat, 0) + value
            else:
                adventurer.equipment[slot] = None
        # Reconstruct skills
        adventurer.skills = [Skill.from_dict(skill_data) for skill_data in data['skills']]
        return adventurer

    def print_equipment(self):
        print("\nCurrent Equipment:")
        for slot, item in self.equipment.items():
            item_name = item.name if item else '[Empty]'
            print(f"{slot.capitalize()}: {item_name}")
