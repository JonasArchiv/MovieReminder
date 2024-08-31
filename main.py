import json
import os

DATA_FILE = 'movie_reminder.json'


def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    return {}


def save_data(data):
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)


def add_entry():
    data = load_data()
    entry_type = input("Film oder Serie hinzufügen? (film/serie): ").strip().lower()

    if entry_type not in ['film', 'serie']:
        print("Ungültige Auswahl.")
        return

    title = input("Titel: ").strip()
    description = input("Beschreibung: ").strip()

    if entry_type == 'film':
        scenes = []
        while True:
            scene = input("Szene (Format hh:mm:ss, Beschreibung) oder Leer lassen zum Beenden: ").strip()
            if not scene:
                break
            scenes.append(scene)
        data[title] = {
            'type': 'film',
            'description': description,
            'scenes': scenes
        }
    elif entry_type == 'serie':
        season = input("Staffel: ").strip()
        episode = input("Folge: ").strip()
        scenes = []
        while True:
            scene = input("Szene (Format hh:mm:ss, Beschreibung) oder Leer lassen zum Beenden: ").strip()
            if not scene:
                break
            scenes.append(scene)
        if title not in data:
            data[title] = {
                'type': 'serie',
                'seasons': {}
            }
        if season not in data[title]['seasons']:
            data[title]['seasons'][season] = {}
        data[title]['seasons'][season][episode] = {
            'description': description,
            'scenes': scenes
        }

    save_data(data)
    print(f"{entry_type.capitalize()} '{title}' hinzugefügt.")



