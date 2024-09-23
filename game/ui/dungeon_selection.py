# game/ui/dungeon_selection.py

from blessed import Terminal

term = Terminal()

def dungeon_selection_screen(dungeons, page_number=1, page_size=5):
    """
    Displays the dungeon selection screen.
    """
    total_pages = (len(dungeons) - 1) // page_size + 1
    while True:
        print(term.clear())
        print(term.bold('DUNGEON SELECTION').center(term.width))
        start_index = (page_number - 1) * page_size
        end_index = start_index + page_size
        current_dungeons = dungeons[start_index:end_index]
        
        print(f'\nAvailable Dungeons (Page {page_number}/{total_pages}):\n')
        print('DUNGEONS:')
        for idx, dungeon in enumerate(current_dungeons, start=1):
            print(f"{idx}. {dungeon['name']} - Lvl {dungeon['level_range']} - Size: {dungeon['size']} - [{dungeon['status']}]")
            print(f"   {dungeon['description']}\n")
        print('0. Next Page\n')
        print('OPTIONS:')
        print('A. Filter/Sort Dungeons')
        print('B. Return to Town Menu\n')
        print('Please select a dungeon by number (0-{0}), or choose an option by letter (A-B): '.format(len(current_dungeons)), end='', flush=True)
        
        val = input().strip()
        if val.isdigit():
            selection = int(val)
            if selection == 0:
                page_number = page_number + 1 if page_number < total_pages else 1
            elif 1 <= selection <= len(current_dungeons):
                selected_dungeon = current_dungeons[selection - 1]
                return selected_dungeon
            else:
                print(term.red('\nInvalid dungeon number. Please try again.'))
                input('\nPress Enter to continue...')
        elif val.lower() == 'a':
            # Implement filter/sort functionality
            print('\n[Filter/Sort functionality is not yet implemented.]')
            input('\nPress Enter to continue...')
        elif val.lower() == 'b':
            # Return to town menu
            return None
        else:
            print(term.red('\nInvalid input. Please try again.'))
            input('\nPress Enter to continue...')

