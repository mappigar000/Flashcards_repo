import json
from core.settings_manager import DATA_DIR

def load_tags():
    with open(DATA_DIR + "/" + "tags.JSON", "r") as f:
        return json.load(f)
        
def update_tags(flashcards):
    tags = set()
    for card in flashcards:
        tags.update(card.get("tags", []))
    tags = sorted(tags)

    with open(DATA_DIR + "/" + "tags.JSON", "w") as f:
        json.dump(list(tags), f)
    return
