from blessed import Terminal

term = Terminal()


def narrative_event(event, party):
    print(term.clear())
    print(term.bold(event['title']).center(term.width))
    print(f"\n{event['description']}\n")
    if 'choices' in event:
        for idx, choice in enumerate(event['choices'], start=1):
            print(f"{idx}. {choice['text']}")
        print('\nPlease select an option: ', end='', flush=True)
        val = input().strip()
        if val.isdigit() and 1 <= int(val) <= len(event['choices']):
            selected_choice = event['choices'][int(val) - 1]
            print(f"\n{selected_choice['outcome']}")
            # Handle the effect
            effect = selected_choice.get('effect')
            if effect == 'heal_party':
                for member in party:
                    if member.is_alive:
                        member.current_hp = member.max_hp
            elif effect == 'gain_item':
                # Assume gain_item adds an item to the shared inventory
                shared_inventory.append(Item(name="Ancient Relic", type="Artifact"))
            # Add other effects as needed
            input('\nPress Enter to continue...')
        else:
            print(term.red('\nInvalid selection. Please try again.'))
            input('\nPress Enter to continue...')
            narrative_event(event, party)
    else:
        input('\nPress Enter to continue...')
