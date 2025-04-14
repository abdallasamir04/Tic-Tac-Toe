import tkinter as tk
from tkinter import messagebox
from gui import TicTacToeGUI

if __name__ == "__main__":
    try:
        game_app = TicTacToeGUI()
    except ImportError as e:
         messagebox.showerror("Import Error", f"Failed to load component: {e}\n\nPlease ensure Pygame is installed (`pip install pygame`).")
    except Exception as e:
        import traceback
        traceback.print_exc()
        messagebox.showerror("Runtime Error", f"An unexpected error occurred:\n\n{e}\n\nSee console for details.")
