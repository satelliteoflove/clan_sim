# game/ui/clan_management.py

from blessed import Terminal
from game.models.adventurer import Adventurer

term = Terminal()

def clan_management_interface(adventurers):
    current_page = 1
    page_size = 10
    total_pages = (len(adventurers) - 1) // page_size + 1

    while True:
        print(term.clear())
        print(term.bold('CLAN MANAGEMENT').center(term.width))
        start_index = (current_page - 1) * page_size
        end_index = start_index + page_size
        current_adventurers = adventurers[start_index:end_index]

        print(f'\nAdventurers (Page {current_page}/{total_pages}):\n')
        for idx, adv in enumerate(current_adventurers, start=1):
            status = 'Healthy' if adv.is_alive else 'Deceased'
            print(f"{idx}. {adv.name} - {adv.char_class} - Lvl {adv.level} - HP: {adv.current_hp}/{adv.max_hp} - Status: {status}")
        print('\n0. Next Page')
        print('OPTIONS:')
        print('A. View Adventurer Details')
        print('B. Form Party')
        print('C. Heal Adventurers')
        print('D. Resurrect Fallen Adventurers')
        print('E. Create New Adventurer')
        print('F. Filter/Sort Adventurers')
        print('G. Return to Town Menu\n')

        print('Please select an option by entering its number or letter: ', end='', flush=True)
        val = input().strip()

        if val.isdigit():
            selection = int(val)
            if selection == 0:
                current_page = current_page + 1 if current_page < total_pages else 1
            elif 1 <= selection <= len(current_adventurers):
                selected_adventurer = current_adventurers[selection - 1]
                view_adventurer_details(selected_adventurer)
            else:
                print(term.red('\nInvalid selection. Please try again.'))
                input('\nPress Enter to continue...')
        elif val.lower() == 'a':
            select_adventurer_for_details(adventurers)
        elif val.lower() == 'b':
            form_party(adventurers)
        elif val.lower() == 'c':
            heal_adventurers(adventurers)
        elif val.lower() == 'd':
            resurrect_adventurers(adventurers)
        elif val.lower() == 'e':
            # Create new adventurer
            new_adv = character_creation()
            if new_adv:
                adventurers.append(new_adv)
        elif val.lower() == 'f':
            # Implement filter/sort functionality
            print('\n[Filter/Sort functionality is not yet implemented.]')
            input('\nPress Enter to continue...')
        elif val.lower() == 'g':
            # Return to town menu
            return
        else:
            print(term.red('\nInvalid input. Please try again.'))
            input('\nPress Enter to continue...')


def select_adventurer_for_details(adventurers):
    while True:
        print(term.clear())
        print(term.bold('View Adventurer Details').center(term.width))
        for idx, adv in enumerate(adventurers, start=1):
            status = 'Alive' if adv.is_alive else 'Deceased'
            print(f"{idx}. {adv.name} - {adv.char_class} - Lvl {adv.level} - Status: {status}")
        print('\n0. Return to Clan Management Menu')
        print('\nPlease select an adventurer to view details (0-{0}): '.format(len(adventurers)), end='', flush=True)
        val = input().strip()
        if val.isdigit():
            selection = int(val)
            if selection == 0:
                break
            elif 1 <= selection <= len(adventurers):
                selected_adventurer = adventurers[selection - 1]
                view_adventurer_details(selected_adventurer)
            else:
                print(term.red('\nInvalid selection. Please try again.'))
                input('\nPress Enter to continue...')
        else:
            print(term.red('\nInvalid input. Please try again.'))
            input('\nPress Enter to continue...')


def view_adventurer_details(adventurer):
    while True:
        print(term.clear())
        print(term.bold(f"{adventurer.name} - Details").center(term.width))
        status = 'Alive' if adventurer.is_alive else 'Deceased'
        print(f"\nClass: {adventurer.char_class}")
        print(f"Level: {adventurer.level}")
        print(f"HP: {adventurer.current_hp}/{adventurer.max_hp}")
        print(f"Status: {status}")
        print("\nStats:")
        for stat, value in adventurer.stats.items():
            print(f"  {stat}: {value}")
        print("\nSkills:")
        if adventurer.skills:
            for skill in adventurer.skills:
                print(f"  {skill.name} (Level {skill.level})")
        else:
            print("  None")
        print("\nEquipment:")
        for slot, item in adventurer.equipment.items():
            item_name = item.name if item else 'None'
            print(f"  {slot}: {item_name}")
        print('\nOPTIONS:')
        print('A. Return to Previous Menu')
        print('B. Heal Adventurer')
        print('C. Resurrect Adventurer' if not adventurer.is_alive else '')
        print('\nPlease select an option: ', end='', flush=True)
        val = input().strip().lower()
        if val == 'a':
            break
        elif val == 'b':
            heal_adventurer(adventurer)
        elif val == 'c' and not adventurer.is_alive:
            resurrect_adventurer(adventurer)
        else:
            print(term.red('\nInvalid selection. Please try again.'))
            input('\nPress Enter to continue...')


def form_party(adventurers):
    # Implement party formation logic
    print('\n[Party formation functionality is not yet implemented.]')
    input('\nPress Enter to continue...')


def heal_adventurer(adventurer):
    if adventurer.is_alive:
        adventurer.current_hp = adventurer.max_hp
        print(f"\n{adventurer.name} has been healed to full health.")
    else:
        print(term.red(f"\n{adventurer.name} cannot be healed because they are deceased."))
    input('\nPress Enter to continue...')


def heal_adventurers(adventurers):
    for adv in adventurers:
        if adv.is_alive:
            adv.current_hp = adv.max_hp
    print("\nAll alive adventurers have been healed to full health.")
    input('\nPress Enter to continue...')


def resurrect_adventurer(adventurer):
    if not adventurer.is_alive:
        success_chance = 0.75  # 75% chance to succeed
        from random import random
        if random() <= success_chance:
            adventurer.is_alive = True
            adventurer.current_hp = int(adventurer.max_hp * 0.5)  # Resurrected at 50% HP
            print(f"\n{adventurer.name} has been resurrected with {adventurer.current_hp} HP.")
        else:
            print(term.red(f"\nResurrection failed. {adventurer.name} remains deceased."))
    else:
        print(term.red(f"\n{adventurer.name} is already alive."))
    input('\nPress Enter to continue...')


def resurrect_adventurers(adventurers):
    any_resurrected = False
    for adv in adventurers:
        if not adv.is_alive:
            resurrect_adventurer(adv)
            any_resurrected = True
    if not any_resurrected:
        print("\nNo deceased adventurers to resurrect.")
        input('\nPress Enter to continue...')
