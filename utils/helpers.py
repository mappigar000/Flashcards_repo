#TODO make load settings more graceful with error handling

import json
import os

SETTINGS_FILE = "settings.json"
DEFAULT_SETIINGS = {
    "flashcardpack": "Default"
}

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open("settings.json", "r") as f:
                boot_settings = json.load(f)
                if boot_settings == "None":
                    return DEFAULT_SETIINGS
                return boot_settings
        except json.JSONDecodeError:
            pass

        return DEFAULT_SETIINGS

def save_settings(settings):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=4)

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
