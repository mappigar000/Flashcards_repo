import json
import os
from core.settings_manager import DATA_DIR
from core.settings_manager import load_settings

settings = load_settings()
FLASHCARD_FILE = os.path.join(DATA_DIR, settings['flashcardpack'])

def load_flashcards(flashcards):
        with open(DATA_DIR + "/" + flashcards, "r") as f:
            return json.load(f)