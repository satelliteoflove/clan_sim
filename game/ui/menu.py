# game/ui/menu.py

from blessed import Terminal

term = Terminal()


def main_menu():
    """
    Displays the main menu and handles user input.
    """
    while True:
        print(term.clear())
        print(term.bold_underline('DUNGEON RPG SIMULATOR').center(term.width))
        print('\n')
        print('1. New Game')
        print('2. Load Game')
        print('3. Options')
        print('4. Quit')
        print('\n')
        print('Please select an option (1-4): ', end='', flush=True)
        
        with term.cbreak():
            val = term.inkey()
        
        if val == '1':
            # Start a new game
            return 'new_game'
        elif val == '2':
            # Load an existing game
            return 'load_game'
        elif val == '3':
            # Open options menu
            options_menu()
        elif val == '4':
            # Quit the game
            confirm = confirm_quit()
            if confirm:
                exit()
        else:
            print(term.red('\nInvalid selection. Please try again.'))
            input('\nPress Enter to continue...')


def options_menu():
    """
    Displays the options menu.
    """
    print(term.clear())
    print(term.bold('Options Menu').center(term.width))
    print('\n[Options would be displayed here]')
    input('\nPress Enter to return to the main menu...')

def confirm_quit():
    """
    Asks the user to confirm quitting the game.
    """
    print('\nAre you sure you want to quit? (Y/N): ', end='', flush=True)
    val = input().strip().lower()
    return val == 'y'

def confirm_quit_to_main_menu():
    """
    Asks the user to confirm returning to the main menu.
    """
    print('\nAre you sure you want to return to the main menu? Unsaved progress will be lost. (Y/N): ', end='', flush=True)
    val = input().strip().lower()
    return val == 'y'
