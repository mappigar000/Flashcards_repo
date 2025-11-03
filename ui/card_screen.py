import json
from tkinter import Toplevel, Text, ttk, messagebox
from core.flashcard_manager import FLASHCARD_FILE
from core.utils import make_grid_expandable, window_sizer

class CardScreen:
    def __init__(self, root, flashcards, settings):
        self.root = root
        self.flashcards = flashcards
        self.settings = settings

        self.win = Toplevel(root)
        self.win.title("Cards")
        self.win.geometry(window_sizer(self.win, 0.6, 0.5))
        make_grid_expandable(self.win, rows=3, cols=2)

        # Left panel: flashcard list
        self.setup_left_panel()

        # Right panel: card details
        self.setup_right_panel()

        # Bottom buttons
        self.setup_bottom_buttons()

    # -------------------------
    # --- UI Setup Methods ---
    # -------------------------
    def setup_left_panel(self):
        self.left = ttk.Frame(self.win, padding=10)
        self.left.grid(row=0, column=0, rowspan=3, sticky="nsew")
        make_grid_expandable(self.left)

        ttk.Label(self.left, text="Flashcards").pack(anchor="w")

        # Treeview
        self.tree = ttk.Treeview(self.left, columns=("Question", "Answer", "Tags"), show="headings")
        self.tree.heading("Question", text="Question")
        self.tree.heading("Answer", text="Answer")
        self.tree.heading("Tags", text="Tags")

        self.tree.column("Question", width=200, anchor="w")
        self.tree.column("Answer", width=200, anchor="w")
        self.tree.column("Tags", width=100, anchor="w")

        # Populate tree
        for card in self.flashcards:
            question = card.get("question", "")
            answer = card.get("answer", "")
            tags = ", ".join(card.get("tags", []))
            self.tree.insert("", "end", values=(question, answer, tags))

        self.tree.pack(expand=True, fill="both")
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

    def setup_right_panel(self):
        self.right = ttk.Frame(self.win, padding=10)
        self.right.grid(row=0, column=1, rowspan=3, sticky="nsew")
        make_grid_expandable(self.right, rows=3, cols=2)

        ttk.Label(self.right, text="Question:").grid(row=0, column=0, sticky="w")
        self.question_text = Text(self.right, height=4, wrap="word")
        self.question_text.grid(row=0, column=1, sticky="nsew")

        ttk.Label(self.right, text="Answer:").grid(row=1, column=0, sticky="w")
        self.answer_text = Text(self.right, height=4, wrap="word")
        self.answer_text.grid(row=1, column=1, sticky="nsew")

        ttk.Label(self.right, text="Tags:").grid(row=2, column=0, sticky="w")
        self.tags_entry = ttk.Entry(self.right)
        self.tags_entry.grid(row=2, column=1, sticky="ew")

    def setup_bottom_buttons(self):
        self.bottom = ttk.Frame(self.win, padding=10)
        self.bottom.grid(row=3, column=0, columnspan=2, sticky="ew")

        ttk.Button(self.bottom, text="Add Card",
                   command=lambda: self.add_card_screen()).pack(side="left", padx=5)
        ttk.Button(self.bottom, text="Edit Card",
                   command=self.edit_card).pack(side="left", padx=5)
        ttk.Button(self.bottom, text="Delete Card",
                   command=self.delete_card).pack(side="left", padx=5)
        ttk.Button(self.bottom, text="Back", command=self.win.destroy).pack(side="right", padx=5)

    # -------------------------
    # --- Functional Methods ---
    # -------------------------
    def on_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        item = self.tree.item(selected[0])
        question, answer, tags = item["values"]

        self.question_text.delete("1.0", "end")
        self.question_text.insert("1.0", question)

        self.answer_text.delete("1.0", "end")
        self.answer_text.insert("1.0", answer)

        self.tags_entry.delete(0, "end")
        self.tags_entry.insert(0, tags)

    def delete_card(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No selection", "Please select a card to delete.")
            self.win.lift()
            self.win.focus_force()
            return

        confirm = messagebox.askyesno("Delete Card", "Are you sure you want to delete this card?")
        self.win.lift()
        self.win.focus_force()
        if not confirm:
            return

        item_id = selected[0]
        item = self.tree.item(item_id)
        question, answer, tags = item["values"]

        # Remove from Treeview
        self.tree.delete(item_id)

        # Remove from flashcards list
        for i, card in enumerate(self.flashcards):
            if (card.get("question", "") == question and
                card.get("answer", "") == answer and
                ", ".join(card.get("tags", [])) == tags):
                del self.flashcards[i]
                break

        # Clear right-side fields
        self.question_text.delete("1.0", "end")
        self.answer_text.delete("1.0", "end")
        self.tags_entry.delete(0, "end")

        # Save to file
        with open(FLASHCARD_FILE, "w") as f:
            json.dump(self.flashcards, f, indent=4)

    def edit_card(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No selection", "Select a card to edit.")
            return

        question = self.question_text.get("1.0", "end").strip()
        answer = self.answer_text.get("1.0", "end").strip()
        tags = self.tags_entry.get().split()

        item_id = selected[0]
        # Update Treeview
        self.tree.item(item_id, values=(question, answer, ", ".join(tags)))

        # Update flashcards list
        idx = self.tree.index(item_id)
        self.flashcards[idx] = {"question": question, "answer": answer, "tags": tags}

        with open(FLASHCARD_FILE, "w") as f:
            json.dump(self.flashcards, f, indent=4)

    def refresh_tree(self):
        self.tree.delete(*self.tree.get_children())
        for card in self.flashcards:
            question = card.get("question", "")
            answer = card.get("answer", "")
            tags = ", ".join(card.get("tags", []))
            self.tree.insert("", "end", values=(question, answer, tags))


    def add_card_screen(self):
        from ui.add_card_screen import AddCardScreen
        AddCardScreen(self.root, self.flashcards, self.refresh_tree)