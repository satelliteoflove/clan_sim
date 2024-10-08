class Item:
    def __init__(self, name, type, slot, attributes=None):
        self.name = name
        self.type = type
        self.slot = slot
        self.attributes = attributes or {}

    def to_dict(self):
        return {
            'name': self.name,
            'type': self.type,
            'slot': self.slot,
            'attributes': self.attributes,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data['name'],
            type=data['type'],
            slot=data['slot'],
            attributes=data.get('attributes', {})
        )
