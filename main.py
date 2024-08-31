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

    tags = input("Tags (durch Kommas getrennt): ").strip().split(',')
    tags = [tag.strip() for tag in tags]

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
            'scenes': scenes,
            'tags': tags
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
            'scenes': scenes,
            'tags': tags
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
            print("Aktuelle Tags:", ', '.join(entry.get('tags', [])))
            new_tags = input("Neue Tags (durch Kommas getrennt): ").strip().split(',')
            entry['tags'] = [tag.strip() for tag in new_tags]
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
                    print("      Tags:", ', '.join(details.get('tags', [])))
                    print("      Szene(n):")
                    for scene in details['scenes']:
                        print(f"        - {scene}")
            season = input("Geben Sie die Staffel ein, die Sie bearbeiten möchten: ").strip()
            episode = input("Geben Sie die Folge ein, die Sie bearbeiten möchten: ").strip()
            if season in data[title]['seasons'] and episode in data[title]['seasons'][season]:
                episode_entry = data[title]['seasons'][season][episode]
                print(f"Aktuelle Beschreibung: {episode_entry['description']}")
                new_description = input("Neue Beschreibung: ").strip()
                episode_entry['description'] = new_description
                print("Aktuelle Tags:", ', '.join(episode_entry.get('tags', [])))
                new_tags = input("Neue Tags (durch Kommas getrennt): ").strip().split(',')
                episode_entry['tags'] = [tag.strip() for tag in new_tags]
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


def retrieve_entry():
    data = load_data()
    title = input("Geben Sie den Titel des Films oder der Serie ein, den Sie abrufen möchten: ").strip()

    if title in data:
        entry = data[title]
        if entry['type'] == 'film':
            print(f"Film: {title}")
            print(f"Beschreibung: {entry['description']}")
            print("Tags:", ', '.join(entry.get('tags', [])))
            print("Szene(n):")
            for scene in entry['scenes']:
                print(f"  - {scene}")
        elif entry['type'] == 'serie':
            print(f"Serie: {title}")
            for season, episodes in entry['seasons'].items():
                print(f"  Staffel {season}:")
                for episode, details in episodes.items():
                    print(f"    Folge {episode}")
                    print(f"      Beschreibung: {details['description']}")
                    print("      Tags:", ', '.join(details.get('tags', [])))
                    print("      Szene(n):")
                    for scene in details['scenes']:
                        print(f"        - {scene}")
    else:
        print("Eintrag nicht gefunden.")


def search_by_tag():
    data = load_data()
    tag = input("Geben Sie den Tag ein, nach dem Sie suchen möchten: ").strip()
    found = False

    for title, entry in data.items():
        if entry['type'] == 'film':
            if tag in entry.get('tags', []):
                print(f"Film: {title}")
                print(f"Beschreibung: {entry['description']}")
                print("Tags:", ', '.join(entry.get('tags', [])))
                print("Szene(n):")
                for scene in entry['scenes']:
                    print(f"  - {scene}")
                found = True
        elif entry['type'] == 'serie':
            for season, episodes in entry['seasons'].items():
                for episode, details in episodes.items():
                    if tag in details.get('tags', []):
                        print(f"Serie: {title}")
                        print(f"  Staffel {season}, Folge {episode}")
                        print(f"    Beschreibung: {details['description']}")
                        print(f"    Tags:", ', '.join(details.get('tags', [])))
                        print("    Szene(n):")
                        for scene in details['scenes']:
                            print(f"      - {scene}")
                        found = True
    if not found:
        print("Kein Eintrag gefunden.")


def main():
    while True:
        print("\nFilm Reminder")
        print("1. Eintag hinzufügen")
        print("2. Abrufen")
        print("3. Bearbeiten")
        print("4. Nach Tags suchen")
        print("5. Beenden")
        choice = input("Wählen Sie eine Option (1/2/3/4/5): ").strip()

        if choice == '1':
            add_entry()
        elif choice == '2':
            retrieve_entry()
        elif choice == '3':
            edit_entry()
        elif choice == '4':
            search_by_tag()
        elif choice == '5':
            break
        else:
            print("Ungültige Auswahl. Bitte versuchen Sie es erneut.")


if __name__ == "__main__":
    main()
