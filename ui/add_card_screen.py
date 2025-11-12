import json
from tkinter import Toplevel, ttk
from core.flashcard_manager import FLASHCARD_FILE
from core.utils import window_sizer, make_grid_expandable

ADD_CARD_ENTRY_WIDTH = 50  # make sure this constant is defined somewhere

class AddCardScreen:
    def __init__(self, root, flashcards, refresh_tree, tags):
        self.root = root
        self.flashcards = flashcards
        self.refresh_tree = refresh_tree
        self.tags = tags

        self.win = Toplevel(self.root)
        self.win.title("Add New Card")
        self.win.geometry(window_sizer(self.win, 0.6, 0.5))
        make_grid_expandable(self.win, rows=0, cols=2)

        self.build_ui()

    def build_ui(self):
        # Labels and entries
        ttk.Label(self.win, text="Question:").grid(row=0, column=0)
        self.question_entry = ttk.Entry(self.win, width=ADD_CARD_ENTRY_WIDTH)
        self.question_entry.grid(row=0, column=1)

        ttk.Label(self.win, text="Answer:").grid(row=1, column=0)
        self.answer_entry = ttk.Entry(self.win, width=ADD_CARD_ENTRY_WIDTH)
        self.answer_entry.grid(row=1, column=1)

        ttk.Label(self.win, text="Tags (space-separated):").grid(row=2, column=0)
        self.tags_entry = ttk.Entry(self.win, width=ADD_CARD_ENTRY_WIDTH)
        self.tags_entry.grid(row=2, column=1)

        # Buttons
        ttk.Button(self.win, text="Back", command=self.on_back).grid(row=4, column=0)
        ttk.Button(self.win, text="Save", command=self.on_save).grid(row=4, column=1)

    def on_save(self):
        question = self.question_entry.get()
        answer = self.answer_entry.get()
        tags = self.tags_entry.get().split()

        self.flashcards.append({"question": question, "answer": answer, "tags": tags})

        with open(FLASHCARD_FILE, "w") as f:
            json.dump(self.flashcards, f, indent=4)

        self.refresh_tree()
        self.win.destroy()

    def on_back(self):
        self.refresh_tree()
        self.win.destroy()