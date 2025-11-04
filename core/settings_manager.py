import os
import json

DATA_DIR = "data"
SETTINGS_FILE = "settings.json"
DEFAULT_SETIINGS = {
    "flashcardpack": "Default"
}

def load_settings():
    if os.path.exists(os.path.join(DATA_DIR, SETTINGS_FILE)):
        try:
            with open(os.path.join(DATA_DIR, SETTINGS_FILE), "r") as f:
                boot_settings = json.load(f)
                if boot_settings == "None":
                    return DEFAULT_SETIINGS
                return boot_settings
        except json.JSONDecodeError:
            pass

        return DEFAULT_SETIINGS
    
def save_settings(settings):
    with open(os.path.join(DATA_DIR, SETTINGS_FILE), "w") as f:
        json.dump(settings, f, indent=4)