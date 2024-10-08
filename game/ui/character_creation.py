# game/ui/character_creation.py

from blessed import Terminal
from game.models.adventurer import Adventurer
from game.data import data_loader

term = Terminal()

def character_creation():
    """
    Handles the character creation process.
    """
    name = get_character_name()
    race = select_race()
    alignment = select_alignment()
    stats = allocate_bonus_points(race)
    available_classes = determine_available_classes(alignment, stats)
    
    if not available_classes:
        print(term.red('\nNo classes available with the current alignment and stats.'))
        print('Please adjust your alignment or reallocate your stats.')
        input('\nPress Enter to restart character creation...')
        return character_creation()
    
    char_class = select_class(available_classes)
    confirm = confirm_character(name, race, alignment, stats, char_class)
    if confirm:
        # Create and return the adventurer object
        adventurer = Adventurer(name, race, alignment, stats, char_class)
        return adventurer
    else:
        return character_creation()

def get_character_name():
    print(term.clear())
    print(term.bold('Character Creation').center(term.width))
    print('\nEnter Character Name: ', end='', flush=True)
    name = input()
    return name.strip()

def select_race():
    races = data_loader.load_races()
    while True:
        print(term.clear())
        print(term.bold('Select Race').center(term.width))
        for idx, race in enumerate(races, start=1):
            print(f"{idx}. {race['name']}")
        print('\nPlease select a race (1-{0}): '.format(len(races)), end='', flush=True)
        val = input()
        if val.isdigit() and 1 <= int(val) <= len(races):
            return races[int(val) - 1]['name']
        else:
            print(term.red('\nInvalid selection. Please try again.'))
            input('\nPress Enter to continue...')

def select_alignment():
    alignments = data_loader.load_alignments()
    while True:
        print(term.clear())
        print(term.bold('Select Alignment').center(term.width))
        for idx, alignment in enumerate(alignments, start=1):
            print(f"{idx}. {alignment['name']}")
        print('\nPlease select an alignment (1-{0}): '.format(len(alignments)), end='', flush=True)
        val = input()
        if val.isdigit() and 1 <= int(val) <= len(alignments):
            return alignments[int(val) - 1]['name']
        else:
            print(term.red('\nInvalid selection. Please try again.'))
            input('\nPress Enter to continue...')

def allocate_bonus_points(race_name):
    race = data_loader.get_race_by_name(race_name)
    base_stats = race['base_stats']
    max_stats = race['max_stats']
    bonus_points = 10
    stats = base_stats.copy()
    
    stat_keys = list(stats.keys())
    stat_letters = {stat[0].lower(): stat for stat in stat_keys}

    while True:
        remaining_points = bonus_points - sum([stats[stat] - base_stats[stat] for stat in stats])
        print(term.clear())
        print(term.bold('Allocate Bonus Points').center(term.width))
        print(f"\nBonus Points Remaining: {remaining_points}")
        print("\nPress the first letter of a stat to add a point, or 'Shift' + letter to remove a point.\n")
        for stat in stat_keys:
            print(f"{stat}: {stats[stat]} [+{stats[stat] - base_stats[stat]}] (Max: {max_stats[stat]})")
        print("\nPress 'Enter' when done.")

        with term.cbreak():
            key = term.inkey()

        if key.name == 'KEY_ENTER':
            if remaining_points == 0:
                return stats
            else:
                print(term.red('\nYou must allocate all bonus points before proceeding.'))
                input('\nPress Enter to continue...')
                continue

        elif key.is_sequence:
            # Handle Shift + Letter
            if key.code and key.name.startswith('KEY_SHIFT_'):
                letter = key.name[-1].lower()
                if letter in stat_letters:
                    stat = stat_letters[letter]
                    if stats[stat] > base_stats[stat]:
                        stats[stat] -= 1
                    else:
                        print(term.red(f"\nCannot reduce {stat} below base value."))
                        input('\nPress Enter to continue...')
                else:
                    print(term.red('\nInvalid stat key. Please try again.'))
                    input('\nPress Enter to continue...')
            else:
                print(term.red('\nInvalid key. Please try again.'))
                input('\nPress Enter to continue...')
        else:
            # Handle single letter keys for adding points
            letter = key.lower()
            if letter in stat_letters:
                stat = stat_letters[letter]
                if remaining_points > 0 and stats[stat] < max_stats[stat]:
                    stats[stat] += 1
                elif stats[stat] >= max_stats[stat]:
                    print(term.red(f"\n{stat} has reached its maximum value."))
                    input('\nPress Enter to continue...')
                else:
                    print(term.red('\nNo bonus points remaining.'))
                    input('\nPress Enter to continue...')
            else:
                print(term.red('\nInvalid stat key. Please try again.'))
                input('\nPress Enter to continue...')

def determine_available_classes(alignment, stats):
    classes = data_loader.load_classes()
    available_classes = []
    for cls in classes:
        if alignment in cls['allowed_alignments'] and all(stats[stat] >= cls['stat_requirements'].get(stat, 0) for stat in stats):
            available_classes.append(cls)
    return available_classes

def select_class(available_classes):
    while True:
        print(term.clear())
        print(term.bold('Select Class').center(term.width))
        for idx, cls in enumerate(available_classes, start=1):
            print(f"{idx}. {cls['name']}")
            print(f"   Requirements: {cls['stat_requirements']}")
        print('\nPlease select a class (1-{0}): '.format(len(available_classes)), end='', flush=True)
        val = input()
        if val.isdigit() and 1 <= int(val) <= len(available_classes):
            return available_classes[int(val) - 1]['name']
        else:
            print(term.red('\nInvalid selection. Please try again.'))
            input('\nPress Enter to continue...')

def confirm_character(name, race, alignment, stats, char_class):
    print(term.clear())
    print(term.bold('Character Summary').center(term.width))
    print(f"\nName: {name}")
    print(f"Race: {race}")
    print(f"Alignment: {alignment}")
    print(f"Class: {char_class}")
    print("\nStats:")
    for stat, value in stats.items():
        print(f"  {stat}: {value}")
    print('\nIs this character acceptable?')
    print('1. Confirm')
    print('2. Redo Character Creation')
    print('3. Generate Random Character')
    print('\nPlease select an option (1-3): ', end='', flush=True)
    val = input()
    if val == '1':
        return True
    elif val == '2':
        return False
    elif val == '3':
        # Implement random character generation if desired
        pass
    else:
        print(term.red('\nInvalid selection. Please try again.'))
        input('\nPress Enter to continue...')
        return confirm_character(name, race, alignment, stats, char_class)

