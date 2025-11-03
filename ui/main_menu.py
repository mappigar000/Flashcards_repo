from tkinter import ttk
from core.utils import make_grid_expandable

def main_menu_screen(app):
    # Clear root window
    for widget in app.root.winfo_children():
        widget.destroy()

    frm = ttk.Frame(app.root, padding=100)
    make_grid_expandable(frm, rows=4, cols=1)
    frm.grid(sticky="nsew")

    ttk.Button(frm, width=100, text="Practice", command=lambda: print("TODO: Practice screen")).grid(column=0, row=0)
    ttk.Button(frm, width=100, text="See Cards", command=app.show_card_screen).grid(column=0, row=1)
    ttk.Button(frm, width=100, text="Settings", command=app.show_settings).grid(column=0, row=2)
    ttk.Button(frm, width=100, text="Quit", command=app.root.destroy).grid(column=0, row=3)
