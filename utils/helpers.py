import json
import os

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open("settings.json", "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            pass

def add_card(flashcards):
    question = input("Type the question:\n")
    answer = input("Type the answer:\n")
    tags_input = input("Enter tags seperated by spaces (all lowercase):\n")
    tags = tags_input.split()

    x = {
        "question": question,
        "answer": answer,
        "tags": tags
    }

    flashcards.append(x)

    with open("flashcards.json", "w") as f:
        json.dump(flashcards, f, indent=4)
