# game/ui/combat.py

from blessed import Terminal
from random import randint

term = Terminal()


def combat_interface(party, enemies):
    combat_over = False
    while not combat_over:
        # Player's turn
        for member in party:
            if member.is_alive:
                print(term.clear())
                print(term.bold('COMBAT').center(term.width))
                print("\nYour Party:")
                for ally in party:
                    status = 'Alive' if ally.is_alive else 'Deceased'
                    print(f"- {ally.name} - HP: {ally.current_hp}/{ally.max_hp} - Status: {status}")
                print("\nEnemies:")
                for idx, enemy in enumerate(enemies, start=1):
                    status = 'Alive' if enemy.is_alive else 'Defeated'
                    print(f"{idx}. {enemy.name} - HP: {enemy.current_hp}/{enemy.max_hp} - Status: {status}")
                print(f"\n{member.name}'s Turn:")
                print("1. Attack")
                print("2. Use Skill")
                print("3. Use Item")
                print("4. Defend")
                print("\nPlease select an action (1-4): ", end='', flush=True)
                val = input().strip()
                if val == '1':
                    # Attack
                    target = select_target(enemies)
                    if target:
                        perform_attack(member, target)
                elif val == '2':
                    # Use Skill (not implemented)
                    print("\nSkills are not yet implemented.")
                    input('\nPress Enter to continue...')
                elif val == '3':
                    # Use Item (not implemented)
                    print("\nItems are not yet implemented.")
                    input('\nPress Enter to continue...')
                elif val == '4':
                    # Defend
                    member.is_defending = True
                    print(f"\n{member.name} is defending and will take reduced damage until next turn.")
                    input('\nPress Enter to continue...')
                else:
                    print(term.red('\nInvalid selection. Please try again.'))
                    input('\nPress Enter to continue...')
                    continue
        # Check if all enemies are defeated
        if all(not enemy.is_alive for enemy in enemies):
            print("\nYou have defeated all enemies!")
            combat_over = True
            continue
        # Enemies' turn
        for enemy in enemies:
            if enemy.is_alive:
                target = select_random_target(party)
                perform_attack(enemy, target)
        # Check if all party members are defeated
        if all(not member.is_alive for member in party):
            print(term.red("\nYour party has been defeated!"))
            combat_over = True


def select_target(enemies):
    alive_enemies = [enemy for enemy in enemies if enemy.is_alive]
    if not alive_enemies:
        return None
    print("\nSelect a target:")
    for idx, enemy in enumerate(alive_enemies, start=1):
        print(f"{idx}. {enemy.name} - HP: {enemy.current_hp}/{enemy.max_hp}")
    print("\nPlease select a target (1-{0}): ".format(len(alive_enemies)), end='', flush=True)
    val = input().strip()
    if val.isdigit():
        selection = int(val)
        if 1 <= selection <= len(alive_enemies):
            return alive_enemies[selection - 1]
        else:
            print(term.red('\nInvalid selection. Please try again.'))
            return select_target(enemies)
    else:
        print(term.red('\nInvalid input. Please try again.'))
        return select_target(enemies)


def perform_attack(attacker, defender):
    damage = calculate_damage(attacker, defender)
    defender.current_hp -= damage
    if defender.current_hp <= 0:
        defender.is_alive = False
        defender.current_hp = 0
        print(f"\n{attacker.name} attacks {defender.name} for {damage} damage. {defender.name} has been defeated!")
    else:
        print(f"\n{attacker.name} attacks {defender.name} for {damage} damage. {defender.name} has {defender.current_hp} HP remaining.")
    input('\nPress Enter to continue...')


def calculate_damage(attacker, defender):
    # Simple damage formula: attacker's Strength minus defender's Endurance
    base_damage = attacker.stats.get('Strength', 5) - defender.stats.get('Endurance', 5)
    if base_damage < 1:
        base_damage = 1
    if defender.is_defending:
        base_damage = base_damage // 2  # Defender takes half damage
        defender.is_defending = False  # Reset defending status
    # Add randomness
    damage = base_damage + randint(-2, 2)
    if damage < 1:
        damage = 1
    return damage


def select_random_target(party):
    alive_members = [member for member in party if member.is_alive]
    if not alive_members:
        return None
    return random.choice(alive_members)
