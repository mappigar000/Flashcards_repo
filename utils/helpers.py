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
ADD_CARD_ENTRY_WIDTH = 50

def window_sizer(root, width_percent, height_percentage):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    window_width = int(screen_width * width_percent)
    window_height = int(screen_height * height_percentage)

    x_position = int((screen_width - window_width) / 2)
    y_position = int((screen_height - window_height) / 2)

    return f"{window_width}x{window_height}+{x_position}+{y_position}"

def make_grid_expandable(widget, rows=1, cols=1):
    for r in range(rows):
        widget.rowconfigure(r, weight=1)
    for c in range(cols):
        widget.columnconfigure(c, weight=1)

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

def practice_sequence():
    return

def settings_screen():
    return

def add_card_screen(root, flashcards):
    win = Toplevel(root)
    win.title("Add New Card")
    win.geometry(window_sizer(win, 0.6, 0.5))
    make_grid_expandable(win, rows=0, cols=2)

    ttk.Label(win, text="Question:").grid(row=0, column=0)
    question_entry = ttk.Entry(win, width=ADD_CARD_ENTRY_WIDTH)
    question_entry.grid(row=0, column=1)

    ttk.Label(win, text="Answer:").grid(row=1, column=0)
    answer_entry = ttk.Entry(win, width=ADD_CARD_ENTRY_WIDTH)
    answer_entry.grid(row=1, column=1)

    ttk.Label(win, text="Tags (space-separated):").grid(row=2, column=0)
    tags_entry = ttk.Entry(win, width=ADD_CARD_ENTRY_WIDTH)
    tags_entry.grid(row=2, column=1)

    def save():
        question = question_entry.get()
        answer = answer_entry.get()
        tags = tags_entry.get().split()
        flashcards.append({"question": question, "answer": answer, "tags": tags})

        with open("flashcards.json", "w") as f:
            json.dump(flashcards, f, indent=4)
        win.destroy()

    ttk.Button(win, text="Back", command=win.destroy).grid(row=4, column=0, columnspan=1)
    ttk.Button(win, text="Save", command=save).grid(row=4, column=1, columnspan=2)

def card_screen(root, flashcards):
    from tkinter import messagebox

    win = Toplevel(root)
    win.title("Cards")
    win.geometry(window_sizer(win, 0.6, 0.5))
    make_grid_expandable(win, rows=3, cols=2)

    # --- Left panel: flashcard list
    left = ttk.Frame(win, padding=10)
    left.grid(row=0, column=0, rowspan=3, sticky="nsew")
    make_grid_expandable(left)

    ttk.Label(left, text="Flashcards").pack(anchor="w")

    # Treeview with question, answer, and tags
    tree = ttk.Treeview(left, columns=("Question", "Answer", "Tags"), show="headings")
    tree.heading("Question", text="Question")
    tree.heading("Answer", text="Answer")
    tree.heading("Tags", text="Tags")

    # Set column widths and behaviors
    tree.column("Question", width=200, anchor="w")
    tree.column("Answer", width=200, anchor="w")
    tree.column("Tags", width=100, anchor="w")

    # Populate treeview
    for card in flashcards:
        question = card.get("question", "")
        answer = card.get("answer", "")
        tags = ", ".join(card.get("tags", []))
        tree.insert("", "end", values=(question, answer, tags))

    tree.pack(expand=True, fill="both")

    # --- Right panel: card details
    right = ttk.Frame(win, padding=10)
    right.grid(row=0, column=1, rowspan=3, sticky="nsew")
    make_grid_expandable(right, rows=3, cols=2)

    ttk.Label(right, text="Question:").grid(row=0, column=0, sticky="w")
    question_text = Text(right, height=4, wrap="word")
    question_text.grid(row=0, column=1, sticky="nsew")

    ttk.Label(right, text="Answer:").grid(row=1, column=0, sticky="w")
    answer_text = Text(right, height=4, wrap="word")
    answer_text.grid(row=1, column=1, sticky="nsew")

    ttk.Label(right, text="Tags:").grid(row=2, column=0, sticky="w")
    tags_entry = ttk.Entry(right)
    tags_entry.grid(row=2, column=1, sticky="ew")

    # --- Populate right panel when selecting a card
    def on_select(event):
        selected = tree.selection()
        if not selected:
            return
        item = tree.item(selected[0])
        question, answer, tags = item["values"]
        question_text.delete("1.0", "end")
        question_text.insert("1.0", question)
        answer_text.delete("1.0", "end")
        answer_text.insert("1.0", answer)
        tags_entry.delete(0, "end")
        tags_entry.insert(0, tags)

    tree.bind("<<TreeviewSelect>>", on_select)

    # --- Delete card function
    def delete_card():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("No selection", "Please select a card to delete.")
            win.lift()
            win.focus_force()
            return

        # Confirm deletion
        confirm = messagebox.askyesno("Delete Card", "Are you sure you want to delete this card?")
        win.lift()
        win.focus_force()
        if not confirm:
            return

        item_id = selected[0]
        item = tree.item(item_id)
        question, answer, tags = item["values"]

        # Remove from Treeview
        tree.delete(item_id)

        # Remove from flashcards list
        for i, card in enumerate(flashcards):
            if (card.get("question", "") == question and
                card.get("answer", "") == answer and
                ", ".join(card.get("tags", [])) == tags):
                del flashcards[i]
                break

        # Clear right-side fields
        question_text.delete("1.0", "end")
        answer_text.delete("1.0", "end")
        tags_entry.delete(0, "end")

        with open("flashcards.json", "w") as f:
            json.dump(flashcards, f, indent=4)

    # --- Bottom buttons
    bottom = ttk.Frame(win, padding=10)
    bottom.grid(row=3, column=0, columnspan=2, sticky="ew")

    ttk.Button(bottom, text="Add Card", command=lambda: add_card_screen(win, flashcards)).pack(side="left", padx=5)
    ttk.Button(bottom, text="Edit Card").pack(side="left", padx=5)
    ttk.Button(bottom, text="Delete Card", command=delete_card).pack(side="left", padx=5)
    ttk.Button(bottom, text="Back", command=win.destroy).pack(side="right", padx=5)
