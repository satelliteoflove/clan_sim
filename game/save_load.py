import json
import os
from game.models.adventurer import Adventurer
from game.models.item import Item
from game.models.party import Party

SAVE_FILE_PATH = os.path.join(os.path.dirname(__file__), 'savegame.json')


def save_game(adventurers, shared_inventory, game_state, parties, active_party):
    data = {
        'adventurers': [adv.to_dict() for adv in adventurers],
        'shared_inventory': [item.to_dict() for item in shared_inventory],
        'game_state': game_state,
        'parties': [serialize_party(party) for party in parties],
        'active_party_index': parties.index(active_party[0]) if active_party[0] in parties else None,
    }
    try:
        with open(SAVE_FILE_PATH, 'w') as f:
            json.dump(data, f, indent=4)
        print("\nGame saved successfully.")
    except Exception as e:
        print(f"\nAn error occurred while saving the game: {e}")


def load_game():
    if not os.path.exists(SAVE_FILE_PATH):
        print("\nNo saved game found.")
        return None
    try:
        with open(SAVE_FILE_PATH, 'r') as f:
            data = json.load(f)
        adventurers = [Adventurer.from_dict(adv_data) for adv_data in data['adventurers']]
        shared_inventory = [Item.from_dict(item_data) for item_data in data['shared_inventory']]
        game_state = data.get('game_state', {})
        parties = [deserialize_party(party_data, adventurers) for party_data in data.get('parties', [])]
        active_party_index = data.get('active_party_index')
        active_party = [parties[active_party_index]] if active_party_index is not None else [None]
        print("\nGame loaded successfully.")
        return adventurers, shared_inventory, game_state, parties, active_party
    except Exception as e:
        print(f"\nAn error occurred while loading the game: {e}")
        return None


def serialize_party(party):
    return {
        'name': party.name,
        'formation': [
            [adv.name if adv else None for adv in row]
            for row in party.formation
        ],
        'party_inventory': [item.to_dict() for item in party.party_inventory]
    }


def deserialize_party(party_data, adventurers):
    party = Party(party_data['name'])
    name_to_adventurer = {adv.name: adv for adv in adventurers}
    formation = party_data['formation']
    for row_idx, row in enumerate(formation):
        for col_idx, adv_name in enumerate(row):
            if adv_name:
                adventurer = name_to_adventurer.get(adv_name)
                if adventurer:
                    party.add_member(adventurer, position=(row_idx, col_idx))
    party.party_inventory = [Item.from_dict(item_data) for item_data in party_data['party_inventory']]
    return party
