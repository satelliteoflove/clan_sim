# game/ui/inventory_management.py

from blessed import Terminal

term = Terminal()

def inventory_management_interface(adventurers, shared_inventory):
    while True:
        print(term.clear())
        print(term.bold('INVENTORY MANAGEMENT').center(term.width))
        print('\nSelect Adventurer:')
        for idx, adv in enumerate(adventurers, start=1):
            print(f"{idx}. {adv.name}")
        print('0. Return to Previous Menu')

        print('\nPlease select an adventurer (0-{0}): '.format(len(adventurers)), end='', flush=True)
        val = input().strip()
        if val.isdigit():
            selection = int(val)
            if selection == 0:
                return
            elif 1 <= selection <= len(adventurers):
                selected_adventurer = adventurers[selection - 1]
                manage_adventurer_equipment(selected_adventurer, shared_inventory)
            else:
                print(term.red('\nInvalid selection. Please try again.'))
                input('\nPress Enter to continue...')
        else:
            print(term.red('\nInvalid input. Please try again.'))
            input('\nPress Enter to continue...')

def manage_adventurer_equipment(adventurer, shared_inventory):
    while True:
        print(term.clear())
        print(term.bold(f"{adventurer.name} - Equipment").center(term.width))
        print('\nEquipment Slots:')
        for idx, (slot, item) in enumerate(adventurer.equipment.items(), start=1):
            item_name = item.name if item else 'None'
            print(f"{idx}. {slot}: {item_name}")
        print('\nOPTIONS:')
        print('A. Equip Item')
        print('B. Unequip Item')
        print('C. Switch Adventurer')
        print('D. Return to Inventory Menu')

        print('\nPlease select an option (A-D): ', end='', flush=True)
        val = input().strip().lower()
        if val == 'a':
            equip_item(adventurer, shared_inventory)
        elif val == 'b':
            unequip_item(adventurer)
        elif val == 'c':
            return  # Go back to select another adventurer
        elif val == 'd':
            return  # Return to main inventory menu
        else:
            print(term.red('\nInvalid selection. Please try again.'))
            input('\nPress Enter to continue...')


def equip_item(adventurer, shared_inventory):
    if not shared_inventory:
        print("\nNo items available in shared inventory to equip.")
        input('\nPress Enter to continue...')
        return
    # Display available items
    print("\nShared Inventory:")
    for idx, item in enumerate(shared_inventory, start=1):
        print(f"{idx}. {item.name} - {item.type}")
    print("0. Cancel")
    print("\nPlease select an item to equip (0-{0}): ".format(len(shared_inventory)), end='', flush=True)
    val = input().strip()
    if val.isdigit():
        selection = int(val)
        if selection == 0:
            return
        elif 1 <= selection <= len(shared_inventory):
            selected_item = shared_inventory.pop(selection - 1)
            slot = selected_item.slot
            if adventurer.equipment.get(slot):
                # Unequip current item
                shared_inventory.append(adventurer.equipment[slot])
            adventurer.equipment[slot] = selected_item
            print(f"\n{selected_item.name} has been equipped to {adventurer.name} in slot {slot}.")
            input('\nPress Enter to continue...')
        else:
            print(term.red('\nInvalid selection. Please try again.'))
            input('\nPress Enter to continue...')
            equip_item(adventurer, shared_inventory)
    else:
        print(term.red('\nInvalid input. Please try again.'))
        input('\nPress Enter to continue...')
        equip_item(adventurer, shared_inventory)


def unequip_item(adventurer, shared_inventory):
    print("\nAdventurer's Equipment:")
    equipped_items = [(slot, item) for slot, item in adventurer.equipment.items() if item]
    if not equipped_items:
        print("\nNo items are currently equipped.")
        input('\nPress Enter to continue...')
        return
    for idx, (slot, item) in enumerate(equipped_items, start=1):
        print(f"{idx}. {slot}: {item.name}")
    print("0. Cancel")
    print("\nPlease select an item to unequip (0-{0}): ".format(len(equipped_items)), end='', flush=True)
    val = input().strip()
    if val.isdigit():
        selection = int(val)
        if selection == 0:
            return
        elif 1 <= selection <= len(equipped_items):
            slot, item = equipped_items[selection - 1]
            shared_inventory.append(item)
            adventurer.equipment[slot] = None
            print(f"\n{item.name} has been unequipped from {slot} and added back to shared inventory.")
            input('\nPress Enter to continue...')
        else:
            print(term.red('\nInvalid selection. Please try again.'))
            input('\nPress Enter to continue...')
            unequip_item(adventurer, shared_inventory)
    else:
        print(term.red('\nInvalid input. Please try again.'))
        input('\nPress Enter to continue...')
        unequip_item(adventurer, shared_inventory)
