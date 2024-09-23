# game/main.py

from game.ui.menu import main_menu, options_menu
from game.ui.character_creation import character_creation
from game.ui.clan_management import clan_management_interface
from game.ui.dungeon_selection import dungeon_selection_screen
from game.ui.dungeon_exploration import dungeon_exploration_interface
from game.ui.inventory_management import inventory_management_interface
from game.models.adventurer import Adventurer
from game.data import data_loader

def main():
    adventurers = []  # List to hold adventurer instances
    shared_inventory = []  # Shared party inventory
    while True:
        action = main_menu()
        if action == 'new_game':
            # Start a new game
            adventurers = []
            print("\nWelcome to Dungeon RPG Simulator!")
            input('\nPress Enter to proceed to character creation...')
            # Allow the player to create their initial adventurers
            initial_adventurer = character_creation()
            if initial_adventurer:
                adventurers.append(initial_adventurer)
                print(f"\n{initial_adventurer.name} has joined your clan!")
                input('\nPress Enter to continue...')
                # Proceed to the clan management interface
                game_loop(adventurers, shared_inventory)
        elif action == 'load_game':
            # Implement load game functionality
            print('\n[Load game functionality is not yet implemented.]')
            input('\nPress Enter to return to the main menu...')
        elif action == 'options':
            options_menu()
        elif action == 'quit':
            confirm = confirm_quit()
            if confirm:
                print('\nThank you for playing Dungeon RPG Simulator!')
                exit()
        else:
            print('\nReturning to main menu...')
            continue

def game_loop(adventurers, shared_inventory):
    while True:
        print("\n=== Town Menu ===")
        print("1. Clan Management")
        print("2. Inventory Management")
        print("3. Dungeon Selection")
        print("4. Save Game")
        print("5. Return to Main Menu")
        print("\nPlease select an option (1-5): ", end='', flush=True)
        val = input().strip()
        if val == '1':
            clan_management_interface(adventurers)
        elif val == '2':
            inventory_management_interface(adventurers, shared_inventory)
        elif val == '3':
            dungeons = load_dungeons()
            selected_dungeon = dungeon_selection_screen(dungeons)
            if selected_dungeon:
                # Form a party before exploring the dungeon
                party = form_party(adventurers)
                if party:
                    # Proceed to dungeon exploration
                    dungeon_exploration_interface(party, selected_dungeon)
                else:
                    print("\nNo party formed. Returning to town menu.")
                    input('\nPress Enter to continue...')
            else:
                print("\nReturning to town menu.")
                input('\nPress Enter to continue...')
        elif val == '4':
            # Implement save game functionality
            print('\n[Save game functionality is not yet implemented.]')
            input('\nPress Enter to continue...')
        elif val == '5':
            confirm = confirm_quit_to_main_menu()
            if confirm:
                break  # Return to main menu
        else:
            print('\nInvalid selection. Please try again.')
            input('\nPress Enter to continue...')

def load_dungeons():
    # Sample dungeon data
    dungeons = [
        {'name': 'Enchanted Forest', 'level_range': '1-3', 'size': 5, 'status': 'Unlocked', 'description': 'A mystical forest filled with magical creatures.'},
        {'name': 'Ancient Ruins', 'level_range': '3-5', 'size': 10, 'status': 'Unlocked', 'description': 'An underground dungeon with lurking dangers.'},
        {'name': 'Dark Swamp', 'level_range': '5-7', 'size': 15, 'status': 'Locked', 'description': 'Unlock by clearing Ancient Ruins.'},
        {'name': 'Crystal Caverns', 'level_range': '7-10', 'size': 20, 'status': 'Locked', 'description': 'Unlock by having an adventurer reach Level 7.'},
        # Add more dungeons as needed
    ]
    return dungeons

def confirm_quit():
    """
    Asks the user to confirm quitting the game.
    """
    print('\nAre you sure you want to quit the game? (Y/N): ', end='', flush=True)
    val = input().strip().lower()
    return val == 'y'

def confirm_quit_to_main_menu():
    """
    Asks the user to confirm returning to the main menu.
    """
    print('\nAre you sure you want to return to the main menu? Unsaved progress will be lost. (Y/N): ', end='', flush=True)
    val = input().strip().lower()
    return val == 'y'

def form_party(adventurers):
    """
    Allows the player to form a party from available adventurers.
    """
    party = []
    max_party_size = 6
    while len(party) < max_party_size:
        print("\nSelect adventurers to add to your party:")
        available_adventurers = [adv for adv in adventurers if adv not in party and adv.is_alive]
        if not available_adventurers:
            print("\nNo more available adventurers to add.")
            break
        for idx, adv in enumerate(available_adventurers, start=1):
            print(f"{idx}. {adv.name} - {adv.char_class} - Lvl {adv.level}")
        print("0. Done forming party")
        print(f"\nCurrent Party Size: {len(party)} / {max_party_size}")
        print("\nPlease select an adventurer to add (0 to finish): ", end='', flush=True)
        val = input().strip()
        if val.isdigit():
            selection = int(val)
            if selection == 0:
                break
            elif 1 <= selection <= len(available_adventurers):
                selected_adv = available_adventurers[selection - 1]
                party.append(selected_adv)
                print(f"\n{selected_adv.name} has been added to the party.")
            else:
                print('\nInvalid selection. Please try again.')
        else:
            print('\nInvalid input. Please try again.')
    if party:
        print("\nParty formation complete.")
        input('\nPress Enter to continue...')
        return party
    else:
        print("\nNo adventurers were added to the party.")
        return None

if __name__ == '__main__':
    main()
