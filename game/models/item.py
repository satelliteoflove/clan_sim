class Item:
    def __init__(self, name, type, slot, attributes=None, compatible_classes=None, compatible_alignments=None):
        self.name = name
        self.type = type
        self.slot = slot
        self.attributes = attributes or {}
        self.compatible_classes = compatible_classes or []
        self.compatible_alignments = compatible_alignments or []

    def is_compatible(self, adventurer):
        class_compatible = not self.compatible_classes or adventurer.char_class in self.compatible_classes
        alignment_compatible = not self.compatible_alignments or adventurer.alignment in self.compatible_alignments
        return class_compatible and alignment_compatible

    def to_dict(self):
        return {
            'name': self.name,
            'type': self.type,
            'slot': self.slot,
            'attributes': self.attributes,
            'compatible_classes': self.compatible_classes,
            'compatible_alignments': self.compatible_alignments
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data['name'],
            type=data['type'],
            slot=data['slot'],
            attributes=data.get('attributes', {}),
            compatible_classes=data.get('compatible_classes', []),
            compatible_alignments=data.get('compatible_alignments', [])
        )
