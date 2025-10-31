import json
from utils.helpers import add_card

def main():
    while True:
        user_input = input("Enter a command\n")

        if user_input == "add":
            add_card()

        elif user_input == "print":
            with open("flashcards.json", "r") as f:
                flashcards = json.load(f)

            print(flashcards)

        elif user_input == "quit":
            break

if __name__ == "__main__":
    main()