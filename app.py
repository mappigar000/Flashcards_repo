import tkinter as tk
from core.settings_manager import load_settings, save_settings
from core.flashcard_manager import load_flashcards
from core.utils import window_sizer, make_grid_expandable
from ui.main_menu import main_menu_screen
from ui.card_screen import CardScreen
from ui.settings_screen import settings_screen


class FlashBabyApp:
    """Main application controller for the FlashBaby app."""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("FlashBaby")
        self.root.geometry(window_sizer(self.root, 0.6, 0.5))
        make_grid_expandable(self.root)

        # Load settings & data
        self.settings = load_settings()
        save_settings(self.settings)
        self.flashcards = load_flashcards(self.settings["flashcardpack"])

        # Start at main menu
        main_menu_screen(self)

    # --- Navigation methods ---
    def show_main_menu(self):
        main_menu_screen(self)

    def show_card_screen(self):
        CardScreen(self.root, self.flashcards, self.settings)

    def show_settings(self):
        settings_screen(self)

    def run(self):
        self.root.mainloop()
