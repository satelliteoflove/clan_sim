# game/data/data_loader.py

import json
import os


def load_races():
    data_path = os.path.join(os.path.dirname(__file__), 'races.json')
    with open(data_path, 'r') as f:
        races = json.load(f)
    return races


def get_race_by_name(name):
    races = load_races()
    for race in races:
        if race['name'].lower() == name.lower():
            return race
    return None


def load_alignments():
    data_path = os.path.join(os.path.dirname(__file__), 'alignments.json')
    with open(data_path, 'r') as f:
        alignments = json.load(f)
    return alignments


def load_classes():
    data_path = os.path.join(os.path.dirname(__file__), 'classes.json')
    with open(data_path, 'r') as f:
        classes = json.load(f)
    return classes


def load_random_event(theme):
    data_path = os.path.join(os.path.dirname(__file__), 'events.json')
    with open(data_path, 'r') as f:
        events = json.load(f)
    theme_events = [event for event in events if event['theme'] == theme]
    return random.choice(theme_events) if theme_events else random.choice(events)
