# game/ui/dungeon_exploration.py

import random
from game.ui.combat import combat_interface
from game.ui.event_narrative import narrative_event
from game.data import data_loader

def dungeon_exploration_interface(party, dungeon):
    turn = 1
    total_turns = dungeon['size']
    event_log = []
    while turn <= total_turns:
        progress = int((turn / total_turns) * 100)
        progress_bar = '[' + '#' * (progress // 10) + '-' * (10 - (progress // 10)) + ']'
        print(term.clear())
        print(term.bold(f"DUNGEON EXPLORATION - Turn {turn}/{total_turns}").center(term.width))
        print(f"\nProgress: {progress_bar} {progress}% towards Boss Encounter\n")
        print("Party Status:")
        for member in party:
            status = 'Alive' if member.is_alive else 'Deceased'
            print(f"- {member.name} - HP: {member.current_hp}/{member.max_hp} - Status: {status}")
        print("\nEvent Log:")
        for event in event_log[-3:]:
            print(f"- {event}")
        print("\nOPTIONS:")
        print("1. Continue Exploration")
        print("2. Return to Town")
        print("3. Access Inventory\n")
        print("Please select an option (1-3): ", end='', flush=True)
        val = input().strip()
        if val == '1':
            # Proceed to next turn
            event = trigger_random_event(party, dungeon)
            event_log.append(event)
            # Check if party is defeated
            if all(not member.is_alive for member in party):
                print(term.red("\nYour party has been defeated!"))
                input('\nPress Enter to return to town...')
                break
            turn += 1
        elif val == '2':
            # Return to town
            print("\nReturning to town...")
            input('\nPress Enter to continue...')
            break
        elif val == '3':
            # Access inventory
            inventory_management_interface(party, shared_inventory)
        else:
            print(term.red('\nInvalid selection. Please try again.'))
            input('\nPress Enter to continue...')
    else:
        # Boss encounter
        print(term.clear())
        print(term.bold(f"DUNGEON EXPLORATION - Turn {total_turns}/{total_turns}").center(term.width))
        print("\nProgress: [##########] 100% towards Boss Encounter\n")
        print(f"- The party encounters the boss of {dungeon['name']}!")
        input('\nPress Enter to initiate the boss battle...')
        # Implement boss battle logic
        boss = data_loader.load_boss_for_dungeon(dungeon['name'])
        combat_interface(party, [boss])
        if all(not member.is_alive for member in party):
            print(term.red("\nYour party has been defeated by the boss!"))
        else:
            print(term.green("\nCongratulations! You have defeated the boss!"))
        input('\nPress Enter to return to town...')


def trigger_random_event(party, dungeon):
    event_chance = 0.3
    combat_chance = 0.5
    random_value = random.random()
    if random_value < event_chance:
        # Trigger narrative event
        event = data_loader.load_random_event(dungeon['theme'])
        narrative_event(event)
        return f"Encountered event: {event['title']}"
    elif random_value < event_chance + combat_chance:
        # Trigger combat encounter
        enemies = data_loader.load_random_enemies(dungeon['theme'])
        combat_interface(party, enemies)
        if all(not member.is_alive for member in party):
            return "Party was defeated in combat."
        else:
            return "Won a combat encounter."
    else:
        # Nothing happens
        return "The party advances deeper into the dungeon."
