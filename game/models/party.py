# game/models/party.py

class Party:
    def __init__(self, name):
        self.name = name
        # Initialize a 3x2 grid: [ [None, None], [None, None], [None, None] ]
        # Each sublist represents a row: Front Row, Middle Row, Back Row
        self.formation = [[None, None] for _ in range(3)]
        self.members = []
        self.party_inventory = [] # Items carried by the party

    def add_member(self, adventurer, position=None):
        """
        Adds an adventurer to the party at the specified position.
        Position is a tuple (row, column), where row and column are 0-indexed.
        """
        if len(self.members) >= 6:
            print("Party is full.")
            return False
        if adventurer in self.members:
            print(f"{adventurer.name} is already in the party.")
            return False
        if position:
            row, col = position
            if self.formation[row][col] is None:
                self.formation[row][col] = adventurer
                self.members.append(adventurer)
                return True
            else:
                print("Position is already occupied.")
                return False
        else:
            # Add to the first available position
            for row in range(3):
                for col in range(2):
                    if self.formation[row][col] is None:
                        self.formation[row][col] = adventurer
                        self.members.append(adventurer)
                        return True
            print("No available positions in formation.")
            return False

    def remove_member(self, adventurer):
        """
        Removes an adventurer from the party and formation.
        """
        if adventurer in self.members:
            for row in range(3):
                for col in range(2):
                    if self.formation[row][col] == adventurer:
                        self.formation[row][col] = None
            self.members.remove(adventurer)
            return True
        else:
            print(f"{adventurer.name} is not in the party.")
            return False

    def move_member(self, from_position, to_position):
        """
        Moves an adventurer within the formation.
        """
        from_row, from_col = from_position
        to_row, to_col = to_position
        if self.formation[from_row][from_col] is None:
            print("No adventurer at the source position.")
            return False
        if self.formation[to_row][to_col] is not None:
            print("Destination position is already occupied.")
            return False
        # Move the adventurer
        self.formation[to_row][to_col] = self.formation[from_row][from_col]
        self.formation[from_row][from_col] = None
        return True

    def get_formation(self):
        """
        Returns the formation grid.
        """
        return self.formation

    def is_full(self):
        return len(self.members) >= 6

    def is_empty(self):
        return len(self.members) == 0

    def print_formation(self):
        """
        Prints the current formation.
        """
        print("\nCurrent Formation:")
        for row_idx, row in enumerate(self.formation):
            row_str = ""
            for col_idx, member in enumerate(row):
                if member:
                    row_str += f"[{member.name}] "
                else:
                    row_str += "[Empty] "
            if row_idx == 0:
                print("Front Row:  " + row_str)
            elif row_idx == 1:
                print("Middle Row: " + row_str)
            else:
                print("Back Row:   " + row_str)
