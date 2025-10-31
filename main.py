import json
from utils.helpers import add_card, save_settings, load_settings

def main():
    with open("flashcards.json", "r") as f:
        flashcards = json.load(f)

    settings = load_settings()
    save_settings(settings)

    while True:
        user_input = input("Enter a command\n")

        if user_input == "add":
            add_card(flashcards)

        elif user_input == "print":
            with open("flashcards.json", "r") as f:
                flashcards = json.load(f)
            print(flashcards)

        elif user_input == "quit":
            break

if __name__ == "__main__":
    main()