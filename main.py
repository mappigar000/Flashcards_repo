import json
from tkinter import *
from tkinter import ttk
from utils.helpers import card_screen, practice_sequence, settings_screen, save_settings, load_settings, window_sizer, make_grid_expandable

def main():
    boot_settings = load_settings()
    save_settings(boot_settings)

    with open("settings.json") as f:
        settings = json.load(f)

    with open(settings['flashcardpack'], "r") as f:
        flashcards = json.load(f)

    root = Tk()
    root.title("FlashBaby")
    root.geometry(window_sizer(root, 0.6, 0.5))
    make_grid_expandable(root)

    frm = ttk.Frame(root, padding=100)
    make_grid_expandable(frm, rows=4, cols=1)
    frm.grid(sticky="nsew")

    ttk.Button(frm, width=100, text="Practice", command=lambda: practice_sequence()).grid(column=0, row=0)
    ttk.Button(frm, width=100, text="See Cards", command=lambda: card_screen(root, flashcards)).grid(column=0, row=1)
    ttk.Button(frm, width=100, text="Settings", command=lambda: settings_screen()).grid(column=0, row=2)
    ttk.Button(frm, width=100, text="Quit", command=root.destroy).grid(column=0, row=3)
    root.mainloop()

if __name__ == "__main__":
    main()