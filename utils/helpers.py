import json

def add_card():
    question = input("Type the question:\n")
    answer = input("Type the answer:\n")
    tags_input = input("Enter tags seperated by spaces (all lowercase):\n")
    tags = tags_input.split()

    x = {
        "question": question,
        "answer": answer,
        "tags": tags
    }

    with open("flashcards.json", "w") as f:
        json.dump(x, f, indent=4)
