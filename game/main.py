from game.save_load import load_game, save_game
from game.ui.character_creation import character_creation
from game.ui.clan_management import clan_management_interface
from game.ui.dungeon_exploration import dungeon_exploration_interface
from game.ui.dungeon_selection import dungeon_selection_screen
from game.ui.inventory_management import inventory_management_interface
from game.ui.menu import main_menu, options_menu


def main():
    adventurers = []
    shared_inventory = []
    game_state = {}
    parties = []
    active_party = [None]  # Using a list to allow mutable reference

    while True:
        action = main_menu()
        if action == "new_game":
            adventurers = []
            shared_inventory = []
            game_state = {}
            parties = []
            active_party[0] = None
            print("\nWelcome to Dungeon RPG Clan Simulator!")
            input("\nPress Enter to proceed to character creation...")
            initial_adventurer = character_creation()
            if initial_adventurer:
                adventurers.append(initial_adventurer)
                print(f"\n{initial_adventurer.name} has joined your clan!")
                input("\nPress Enter to continue...")
                game_loop(
                    adventurers,
                    shared_inventory,
                    game_state,
                    parties,
                    active_party,
                )
        elif action == "load_game":
            # Load game logic
            result = load_game()
            if result:
                (
                    adventurers,
                    shared_inventory,
                    game_state,
                    parties,
                    active_party_loaded,
                ) = result
                active_party[0] = (
                    active_party_loaded[0] if active_party_loaded else None
                )
                game_loop(
                    adventurers,
                    shared_inventory,
                    game_state,
                    parties,
                    active_party,
                )
            else:
                input("\nPress Enter to return to the main menu...")
        elif action == "options":
            options_menu()
        elif action == "quit":
            confirm = confirm_quit()
            if confirm:
                print("\nThank you for playing Dungeon RPG Clan Simulator!")
                exit()
        else:
            print("\nReturning to main menu...")
            continue


def game_loop(adventurers, shared_inventory, game_state, parties, active_party):
    while True:
        print("\n=== Town Menu ===")
        print("1. Clan Management")
        print("2. Inventory Management")
        print("3. Dungeon Selection")
        print("4. Save Game")
        print("5. Return to Main Menu")
        print("\nPlease select an option (1-5): ", end="", flush=True)
        val = input().strip()
        if val == "1":
            clan_management_interface(adventurers, parties, active_party)
        elif val == "2":
            if active_party[0]:
                inventory_management_interface(
                    active_party[0].members, shared_inventory
                )
            else:
                print(
                    "\nNo active party. Please set an active party in Clan Management."
                )
                input("\nPress Enter to continue...")
        elif val == "3":
            if active_party[0]:
                dungeons = load_dungeons()
                selected_dungeon = dungeon_selection_screen(dungeons)
                if selected_dungeon:
                    dungeon_exploration_interface(
                        active_party[0], selected_dungeon
                    )
                else:
                    print("\nReturning to town menu.")
                    input("\nPress Enter to continue...")
            else:
                print(
                    "\nNo active party. Please set an active party in Clan Management."
                )
                input("\nPress Enter to continue...")
        elif val == "4":
            save_game(
                adventurers, shared_inventory, game_state, parties, active_party
            )
            input("\nPress Enter to continue...")
        elif val == "5":
            confirm = confirm_quit_to_main_menu()
            if confirm:
                break  # Return to main menu
        else:
            print("\nInvalid selection. Please try again.")
            input("\nPress Enter to continue...")


def load_dungeons():
    # Sample dungeon data
    dungeons = [
        {
            "name": "Enchanted Forest",
            "level_range": "1-3",
            "size": 5,
            "status": "Unlocked",
            "description": "A mystical forest filled with magical creatures.",
            "theme": "Enchanted Forest",
        },
        {
            "name": "Ancient Ruins",
            "level_range": "3-5",
            "size": 10,
            "status": "Unlocked",
            "description": "An underground dungeon with lurking dangers.",
            "theme": "Ancient Ruins",
        },
        {
            "name": "Dark Swamp",
            "level_range": "5-7",
            "size": 15,
            "status": "Locked",
            "description": "Unlock by clearing Ancient Ruins.",
            "theme": "Dark Swamp",
        },
        {
            "name": "Crystal Caverns",
            "level_range": "7-10",
            "size": 20,
            "status": "Locked",
            "description": "Unlock by having an adventurer reach Level 7.",
            "theme": "Crystal Caverns",
        },
        # Add more dungeons as needed
    ]
    return dungeons


def confirm_quit():
    """
    Asks the user to confirm quitting the game.
    """
    print(
        "\nAre you sure you want to quit the game? (Y/N): ", end="", flush=True
    )
    val = input().strip().lower()
    return val == "y"


def confirm_quit_to_main_menu():
    """
    Asks the user to confirm returning to the main menu.
    """
    print(
        "\nAre you sure you want to return to the main menu? Unsaved progress will be lost. (Y/N): ",
        end="",
        flush=True,
    )
    val = input().strip().lower()
    return val == "y"


if __name__ == "__main__":
    main()
