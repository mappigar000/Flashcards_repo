import json
from tkinter import *
from tkinter import ttk
from utils.helpers import add_card, save_settings, load_settings

def main():
    boot_settings = load_settings()
    save_settings(boot_settings)

    with open("settings.json") as f:
        settings = json.load(f)

    with open(settings['flashcardpack'], "r") as f:
        flashcards = json.load(f)

    root = Tk()
    root.title("FlashBaby")
    frm = ttk.Frame(root, padding=100)
    frm.grid()
    ttk.Button(frm, text="add card", command=lambda: add_card(root, flashcards)).grid(column=0, row=0)
    ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=0)
    root.mainloop()
'''
    while True:
        user_input = input("Enter a command\n")

        if user_input == "add":
            add_card(flashcards)

        elif user_input == "print":
            with open(settings['flashcardpack'], "r") as f:
                flashcards = json.load(f)
            print(flashcards)

        elif user_input == "quit":
            break
'''
if __name__ == "__main__":
    main()