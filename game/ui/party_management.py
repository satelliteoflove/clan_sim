from blessed import Terminal
from game.ui.equipment_management import equip_adventurer

term = Terminal()

def party_management_interface(party):
    while True:
        print(term.clear())
        print(term.bold(f"Party Management - {party.name}").center(term.width))
        print("\nParty Members:")
        for idx, member in enumerate(party.members, start=1):
            print(f"{idx}. {member.name} - {member.char_class}")
        print("\n0. Return to previous menu")

        choice = input("\nSelect a party member to manage: ").strip()
        if choice == '0':
            break
        elif choice.isdigit() and 1 <= int(choice) <= len(party.members):
            selected_member = party.members[int(choice) - 1]
            equip_adventurer(selected_member, party.party_inventory)
        else:
            print("Invalid selection. Please try again.")
            input("Press Enter to continue...")
