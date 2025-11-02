#TODO make load settings more graceful with error handling
#     make better print function

import json
from tkinter import *
from tkinter import ttk
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

def add_card(root, flashcards):
    win = Toplevel(root)
    win.title("Add New Card")

    ttk.Label(win, text="Question:").grid(row=0, column=0)
    question_entry = ttk.Entry(win, width=50)
    question_entry.grid(row=0, column=1)

    ttk.Label(win, text="Answer:").grid(row=1, column=0)
    answer_entry = ttk.Entry(win, width=50)
    answer_entry.grid(row=1, column=1)

    ttk.Label(win, text="Tags (space-separated):").grid(row=2, column=0)
    tags_entry = ttk.Entry(win, width=50)
    tags_entry.grid(row=2, column=1)

    def save():
        question = question_entry.get()
        answer = answer_entry.get()
        tags = tags_entry.get().split()
        flashcards.append({"question": question, "answer": answer, "tags": tags})

        with open("flashcards.json", "w") as f:
            json.dump(flashcards, f, indent=4)
        win.destroy()

    ttk.Button(win, text="Save", command=save).grid(row=3, column=0, columnspan=2)
