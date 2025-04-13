
import tkinter as tk
from tkinter import messagebox
from gui import TicTacToeGUI

if __name__ == "__main__":
    try:
        print("Starting Tic-Tac-Toe Pro...")
        game_app = TicTacToeGUI()
        print("Game window closed.") 
    except ImportError as e:
         print(f"\n--- IMPORT ERROR ---")
         print(f"Failed to import required module: {e}")
         print("Please ensure all dependencies are installed:")
         print(" - Tkinter (usually built-in)")
         print(" - Pygame (`pip install pygame`)")
         messagebox.showerror("Import Error", f"Failed to load component: {e}\n\nPlease ensure Pygame is installed (`pip install pygame`).")
    except Exception as e:
        print(f"\n--- UNEXPECTED ERROR ---")
        print(f"An unexpected error occurred: {e}")
        import traceback
        traceback.print_exc()
        messagebox.showerror("Runtime Error", f"An unexpected error occurred:\n\n{e}\n\nSee console for details.")