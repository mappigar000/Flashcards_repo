import random
from tkinter import Toplevel, Text, ttk, messagebox, StringVar, Label, Button
from core.flashcard_manager import FLASHCARD_FILE
from core.utils import make_grid_expandable, window_sizer

class PracticeScreen:
    def __init__(self, root, flashcards, settings, tags):
        self.root = root
        self.flashcards = flashcards
        self.settings = settings
        self.tags = tags

        random.shuffle(self.flashcards)

        self.current_index = 0
        self.showing_answer = False

        self.win = Toplevel(root)
        self.win.title("Practice")
        self.win.geometry(window_sizer(self.win, 0.6, 0.5))
        make_grid_expandable(self.win, rows=3, cols=3)

        self.setup_card_display()
        self.setup_bottom_buttons()
        self.bind_keys()
        self.win.focus_set()

        self.load_card()

    def setup_card_display(self):
        """Create widgets for displaying question and answer."""
        self.card_text = StringVar()

        self.card_label = Label(
            self.win,
            textvariable=self.card_text,
            font=("Arial", 16),
            wraplength=500,
            justify="center"
        )
        self.card_label.grid(row=0, column=0, columnspan=3, padx=10, pady=20, sticky="nsew")

        self.show_answer_btn = ttk.Button(
            self.win, text="Show Answer", command=self.toggle_answer
        )
        self.show_answer_btn.grid(row=1, column=1, pady=10)

    def setup_bottom_buttons(self):
        """Buttons for navigation and marking correctness."""
        self.correct_btn = ttk.Button(
            self.win, text="Correct", command=lambda: self.next_card(True)
        )
        self.correct_btn.grid(row=3, column=0, pady=20)

        self.skip_btn = ttk.Button(
            self.win, text="Skip", command=lambda: self.next_card(None)
        )
        self.skip_btn.grid(row=3, column=1, pady=20)

        self.incorrect_btn = ttk.Button(
            self.win, text="Incorrect", command=lambda: self.next_card(False)
        )
        self.incorrect_btn.grid(row=3, column=2, pady=20)

    def bind_keys(self):
        """Bind keyboard shortcuts for smooth navigation."""
        self.win.bind("<space>", self._toggle_answer_key)
        self.win.bind("<Right>", self._correct_key)
        self.win.bind("<Left>", self._incorrect_key)
        self.win.bind("<Down>", self._skip_key)
        self.win.bind("<Escape>", lambda e: self.win.destroy())

    # Each of these wrappers consumes the event
    def _toggle_answer_key(self, event):
        self.toggle_answer()
        return "break"

    def _correct_key(self, event):
        self.next_card(True)
        return "break"

    def _incorrect_key(self, event):
        self.next_card(False)
        return "break"

    def _skip_key(self, event):
        self.next_card(None)
        return "break"


    def load_card(self):
        """Display the current card's question."""
        if not self.flashcards:
            messagebox.showinfo("No Cards", "No flashcards available to practice.")
            self.win.destroy()
            return

        card = self.flashcards[self.current_index]
        self.card_text.set(card["question"])
        self.showing_answer = False
        self.show_answer_btn.config(text="Show Answer")

    def toggle_answer(self):
        """Toggle between showing question and answer."""
        card = self.flashcards[self.current_index]
        if self.showing_answer:
            self.card_text.set(card["question"])
            self.show_answer_btn.config(text="Show Answer")
        else:
            self.card_text.set(card["answer"])
            self.show_answer_btn.config(text="Hide Answer")
        self.showing_answer = not self.showing_answer

        self.win.focus_set()

    def next_card(self, correct):
        """Handle navigation to next card."""
        # Optional: record result (could save to settings or stats)
        self.current_index = (self.current_index + 1) % len(self.flashcards)
        self.load_card()

        self.win.focus_set()