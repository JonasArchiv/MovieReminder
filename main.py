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


def edit_entry():
    data = load_data()
    title = input("Geben Sie den Titel des Films oder der Serie ein, den Sie bearbeiten möchten: ").strip()

    if title in data:
        entry = data[title]
        if entry['type'] == 'film':
            print(f"Aktuelle Beschreibung: {entry['description']}")
            new_description = input("Neue Beschreibung: ").strip()
            entry['description'] = new_description
            print("Aktuelle Szenen:")
            for i, scene in enumerate(entry['scenes']):
                print(f"  {i + 1}. {scene}")
            entry['scenes'] = []
            while True:
                scene = input("Szene (Format hh:mm:ss, Beschreibung) oder Leer lassen zum Beenden: ").strip()
                if not scene:
                    break
                entry['scenes'].append(scene)
        elif entry['type'] == 'serie':
            print(f"Aktuelle Daten für Serie '{title}':")
            for season, episodes in entry['seasons'].items():
                print(f"  Staffel {season}:")
                for episode, details in episodes.items():
                    print(f"    Folge {episode}")
                    print(f"      Beschreibung: {details['description']}")
                    print("      Szene(n):")
                    for scene in details['scenes']:
                        print(f"        - {scene}")
            season = input("Geben Sie die Staffel ein, die Sie bearbeiten möchten: ").strip()
            episode = input("Geben Sie die Folge ein, die Sie bearbeiten möchten: ").strip()
            if season in entry['seasons'] and episode in entry['seasons'][season]:
                episode_entry = entry['seasons'][season][episode]
                print(f"Aktuelle Beschreibung: {episode_entry['description']}")
                new_description = input("Neue Beschreibung: ").strip()
                episode_entry['description'] = new_description
                print("Aktuelle Szenen:")
                for i, scene in enumerate(episode_entry['scenes']):
                    print(f"  {i + 1}. {scene}")
                episode_entry['scenes'] = []
                while True:
                    scene = input("Szene (Format hh:mm:ss, Beschreibung) oder Leer lassen zum Beenden: ").strip()
                    if not scene:
                        break
                    episode_entry['scenes'].append(scene)
            else:
                print("Staffel oder Folge nicht gefunden.")

        save_data(data)
        print(f"{title} erfolgreich bearbeitet.")
    else:
        print("Eintrag nicht gefunden.")


