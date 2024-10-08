from blessed import Terminal
from game.ui.character_creation import character_creation
from game.models.adventurer import Adventurer
from game.models.party import Party


term = Terminal()


def clan_management_interface(adventurers, parties, active_party):
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
        print('B. Manage Parties')
        print('C. Heal Adventurers')
        print('D. Resurrect Fallen Adventurers')
        print('E. Create New Adventurer')
        print('F. Filter/Sort Adventurers')
        print('G. Return to Town Menu\n')

        print('Please select an option by entering its number or letter: ', end='', flush=True)
        val = input().strip().lower()

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
        elif val == 'a':
            select_adventurer_for_details(adventurers)
        elif val == 'b':
            manage_parties_interface(adventurers, parties, active_party)
        elif val == 'c':
            heal_adventurers(adventurers)
        elif val == 'd':
            resurrect_adventurers(adventurers)
        elif val == 'e':
            # Create new adventurer
            new_adv = character_creation()
            if new_adv:
                adventurers.append(new_adv)
                print(f"\n{new_adv.name} has joined your clan!")
                input('\nPress Enter to continue...')
        elif val == 'f':
            # Implement filter/sort functionality
            print('\n[Filter/Sort functionality is not yet implemented.]')
            input('\nPress Enter to continue...')
        elif val == 'g':
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
        if adventurer.is_alive:
            print('B. Heal Adventurer')
        else:
            print('C. Resurrect Adventurer')
        print('\nPlease select an option: ', end='', flush=True)
        val = input().strip().lower()
        if val == 'a':
            break
        elif val == 'b' and adventurer.is_alive:
            heal_adventurer(adventurer)
        elif val == 'c' and not adventurer.is_alive:
            resurrect_adventurer(adventurer)
        else:
            print(term.red('\nInvalid selection. Please try again.'))
            input('\nPress Enter to continue...')


def heal_adventurer(adventurer):
    adventurer.current_hp = adventurer.max_hp
    print(f"\n{adventurer.name} has been healed to full health.")
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


def heal_adventurers(adventurers):
    any_healed = False
    for adv in adventurers:
        if adv.is_alive and adv.current_hp < adv.max_hp:
            adv.current_hp = adv.max_hp
            any_healed = True
    if any_healed:
        print("\nAll alive adventurers have been healed to full health.")
    else:
        print("\nAll alive adventurers are already at full health.")
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


def manage_parties_interface(adventurers, parties, active_party):
    while True:
        print(term.clear())
        print(term.bold('MANAGE PARTIES').center(term.width))
        print('\nParties:')
        for idx, party in enumerate(parties, start=1):
            status = 'Active' if party == active_party else 'In Town'
            print(f"{idx}. {party.name} - Members: {len(party.members)} - {status}")
        print('\nOPTIONS:')
        print('A. Create New Party')
        print('B. Edit Party')
        print('C. Set Active Party')
        print('D. Delete Party')
        print('E. Return to Clan Management\n')

        print('Please select an option by entering its number or letter: ', end='', flush=True)
        val = input().strip().lower()
        if val.isdigit():
            selection = int(val)
            if 1 <= selection <= len(parties):
                selected_party = parties[selection - 1]
                edit_party_interface(adventurers, selected_party)
            else:
                print(term.red('\nInvalid selection. Please try again.'))
                input('\nPress Enter to continue...')
        elif val == 'a':
            create_new_party(adventurers, parties)
        elif val == 'b':
            edit_existing_party(adventurers, parties)
        elif val == 'c':
            set_active_party(parties, active_party)
        elif val == 'd':
            delete_party(parties, active_party)
        elif val == 'e':
            return
        else:
            print(term.red('\nInvalid input. Please try again.'))
            input('\nPress Enter to continue...')


def create_new_party(adventurers, parties):
    print('\nEnter a name for the new party: ', end='', flush=True)
    name = input().strip()
    new_party = Party(name)
    parties.append(new_party)
    print(f"\nParty '{name}' has been created.")
    input('\nPress Enter to continue...')
    edit_party_interface(adventurers, new_party)


def edit_party_interface(adventurers, party):
    while True:
        print(term.clear())
        print(term.bold(f"EDIT PARTY - {party.name}").center(term.width))
        party.print_formation()
        print('\nOPTIONS:')
        print('A. Add Adventurer')
        print('B. Remove Adventurer')
        print('C. Rearrange Formation')
        print('D. Return to Parties Menu\n')

        print('Please select an option: ', end='', flush=True)
        val = input().strip().lower()
        if val == 'a':
            add_adventurer_to_party(adventurers, party)
        elif val == 'b':
            remove_adventurer_from_party(party)
        elif val == 'c':
            rearrange_party_formation(party)
        elif val == 'd':
            break
        else:
            print(term.red('\nInvalid selection. Please try again.'))
            input('\nPress Enter to continue...')


def add_adventurer_to_party(adventurers, party):
    available_adventurers = [adv for adv in adventurers if adv not in party.members and adv.is_alive]
    if not available_adventurers:
        print("\nNo available adventurers to add.")
        input('\nPress Enter to continue...')
        return

    print('\nAvailable Adventurers:')
    for idx, adv in enumerate(available_adventurers, start=1):
        status = 'Healthy' if adv.is_alive else 'Deceased'
        print(f"{idx}. {adv.name} - {adv.char_class} - Lvl {adv.level} - Status: {status}")
    print('\n0. Cancel')

    while True:
        print('\nSelect an adventurer to add: ', end='', flush=True)
        val = input().strip()
        if val.isdigit():
            selection = int(val)
            if selection == 0:
                return
            elif 1 <= selection <= len(available_adventurers):
                selected_adv = available_adventurers[selection - 1]
                break
            else:
                print(term.red('\nInvalid selection. Please enter a number corresponding to an adventurer.'))
        else:
            print(term.red('\nInvalid input. Please enter a numeric value.'))

    while True:
        # Display Current Formation with Row and Column Numbers
        print('\nCurrent Formation:')
        print(f"{'':10}Column 1    Column 2")
        rows = ['Front Row', 'Middle Row', 'Back Row']
        for idx, row_name in enumerate(rows, start=1):
            # Assuming party.formation is a 3x2 grid (list of lists)
            # If not, adjust accordingly
            front = party.formation[idx - 1][0].name if party.formation[idx - 1][0] else '[Empty]'
            back = party.formation[idx - 1][1].name if party.formation[idx - 1][1] else '[Empty]'
            print(f"Row {idx}. {row_name}: {front:<10} {back:<10}")

        print('\nEnter position to place the adventurer by specifying the row and column numbers separated by a comma (e.g., 1,2): ', end='', flush=True)
        pos_input = input().strip()
        try:
            row_str, col_str = pos_input.split(',')
            row = int(row_str.strip()) - 1  # Convert to 0-based index
            col = int(col_str.strip()) - 1  # Convert to 0-based index

            if 0 <= row <= 2 and 0 <= col <= 1:
                if party.formation[row][col] is not None:
                    print(term.red('\nThat position is already occupied. Please choose another position.'))
                else:
                    success = party.add_member(selected_adv, position=(row, col))
                    if success:
                        print(f"\n{selected_adv.name} added to the party at position (Row {row + 1}, Column {col + 1}).")
                        input('\nPress Enter to continue...')
                        return
                    else:
                        print(term.red('\nFailed to add the adventurer to the party. Please try again.'))
            else:
                print(term.red('\nInvalid position. Rows are 1-3 and columns are 1-2. Please try again.'))
        except ValueError:
            print(term.red('\nInvalid input format. Please enter as row,column (e.g., 1,2).'))

    input('\nPress Enter to continue...')


def remove_adventurer_from_party(party):
    if not party.members:
        print("\nNo adventurers in the party.")
        input('\nPress Enter to continue...')
        return
    print('\nParty Members:')
    for idx, adv in enumerate(party.members, start=1):
        print(f"{idx}. {adv.name}")
    print('\n0. Cancel')
    print('\nSelect an adventurer to remove: ', end='', flush=True)
    val = input().strip()
    if val.isdigit():
        selection = int(val)
        if selection == 0:
            return
        elif 1 <= selection <= len(party.members):
            selected_adv = party.members[selection - 1]
            party.remove_member(selected_adv)
            print(f"\n{selected_adv.name} has been removed from the party.")
            input('\nPress Enter to continue...')
        else:
            print(term.red('\nInvalid selection. Please try again.'))
            input('\nPress Enter to continue...')
    else:
        print(term.red('\nInvalid input. Please try again.'))
        input('\nPress Enter to continue...')


def rearrange_party_formation(party):
    party.print_formation()
    print('\nEnter the position to move from (row,column): ', end='', flush=True)
    from_input = input().strip()
    print('Enter the position to move to (row,column): ', end='', flush=True)
    to_input = input().strip()
    try:
        from_row_str, from_col_str = from_input.split(',')
        to_row_str, to_col_str = to_input.split(',')
        from_row = int(from_row_str) - 1
        from_col = int(from_col_str) - 1
        to_row = int(to_row_str) - 1
        to_col = int(to_col_str) - 1
        if all(0 <= idx <= 2 for idx in [from_row, to_row]) and all(0 <= idx <= 1 for idx in [from_col, to_col]):
            success = party.move_member((from_row, from_col), (to_row, to_col))
            if success:
                print("\nAdventurer moved successfully.")
            input('\nPress Enter to continue...')
        else:
            print(term.red('\nInvalid positions. Rows are 1-3, columns are 1-2.'))
            input('\nPress Enter to continue...')
    except ValueError:
        print(term.red('\nInvalid input format. Please enter as row,column (e.g., 1,1).'))
        input('\nPress Enter to continue...')


def set_active_party(parties, active_party):
    print('\nSelect a party to set as active:')
    for idx, party in enumerate(parties, start=1):
        print(f"{idx}. {party.name}")
    print('\n0. Cancel')
    print('\nYour choice: ', end='', flush=True)
    val = input().strip()
    if val.isdigit():
        selection = int(val)
        if selection == 0:
            return
        elif 1 <= selection <= len(parties):
            new_active_party = parties[selection - 1]
            active_party[0] = new_active_party  # Use a mutable type like list to allow reassignment
            print(f"\n{new_active_party.name} is now the active party.")
            input('\nPress Enter to continue...')
        else:
            print(term.red('\nInvalid selection. Please try again.'))
            input('\nPress Enter to continue...')
    else:
        print(term.red('\nInvalid input. Please try again.'))
        input('\nPress Enter to continue...')


def delete_party(parties, active_party):
    print('\nSelect a party to delete:')
    for idx, party in enumerate(parties, start=1):
        status = 'Active' if party == active_party[0] else 'In Town'
        print(f"{idx}. {party.name} - {status}")
    print('\n0. Cancel')
    print('\nYour choice: ', end='', flush=True)
    val = input().strip()
    if val.isdigit():
        selection = int(val)
        if selection == 0:
            return
        elif 1 <= selection <= len(parties):
            party_to_delete = parties[selection - 1]
            if party_to_delete == active_party[0]:
                print(term.red("\nCannot delete the active party. Set another party as active first."))
                input('\nPress Enter to continue...')
            else:
                parties.remove(party_to_delete)
                print(f"\nParty '{party_to_delete.name}' has been deleted.")
                input('\nPress Enter to continue...')
        else:
            print(term.red('\nInvalid selection. Please try again.'))
            input('\nPress Enter to continue...')
    else:
        print(term.red('\nInvalid input. Please try again.'))
        input('\nPress Enter to continue...')
