      
# 🎮 Tic-Tac-Toe Game

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/Language-Python-yellow.svg)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-orange.svg)
![Pygame](https://img.shields.io/badge/Sound-Pygame-red.svg)

A classic **Tic-Tac-Toe** game implemented with a graphical user interface using **Python** and **Tkinter**.
Play against an AI opponent with adjustable difficulty levels, enjoy various visual themes, and experience optional sound effects (requires Pygame).
This project was developed by **_Abdalla Samir_**.

---

## 🚀 Features

*   **Graphical User Interface (GUI):** Clean and intuitive interface built with Tkinter, featuring a 3x3 game grid and control buttons.
*   **Intelligent AI Opponent:** Play against an AI with three difficulty levels:
    *   **Easy:** Makes random valid moves.
    *   **Medium:** Blocks player wins, seeks its own wins, otherwise plays randomly or uses basic strategy.
    *   **Hard:** Implements the **Minimax algorithm** with alpha-beta pruning for optimal move selection.
*   **Customizable Themes:** Choose from six different visual themes (e.g., Sci-Fi, Retro, Forest, Dark Mode) to change the look and feel.
*   **Sound Effects:** Optional sound feedback for clicks, wins, and losses (requires Pygame installation).
*   **Player Options:** Select your preferred symbol (X or O) and choose whether to play first or second.
*   **Score Tracking:** Keeps track of wins for the Player, AI, and the number of Draw games.
*   **Game Controls:** Easily restart the game, change difficulty, switch themes, or exit the application.

---

## ▶️ How to Play

1.  **Launch:** Run the `main.py` script using Python.
2.  **Setup:** A setup window appears. Choose your symbol (X or O) and whether you want to play first or second. Click "Start Game".
3.  **Gameplay:**
    *   Click on an empty square in the 3x3 grid to place your symbol.
    *   The AI will automatically make its move after a short delay (on Medium/Hard difficulty).
    *   The first player to get three of their symbols in a row (horizontally, vertically, or diagonally) wins.
    *   If all squares are filled and no one has won, the game is a draw.
4.  **Controls:**
    *   **Restart:** Click the "Restart" button to start a new game with the current settings and scores.
    *   **Difficulty:** Use the dropdown menu to select Easy, Medium, or Hard AI difficulty (restarts the game).
    *   **Theme:** Use the dropdown menu to change the visual theme instantly.
    *   **Exit:** Click the "Exit" button to close the application.
5.  **Scoreboard:** The scores for Player, Draws, and AI are displayed at the bottom.

---

## 🛠️ How It Works

*   **GUI (`gui.py`):** Manages the main window, grid buttons, labels, control widgets, and user interactions using Tkinter. Handles the game loop visually.
*   **Game Logic (`game_logic.py`):** Contains functions for board initialization, checking for valid moves, determining win/draw conditions, and implementing the AI logic (random, basic strategy, Minimax).
*   **Theming (`themes.py`):** Defines color palettes for different UI elements in a dictionary structure. The GUI module reads and applies these themes.
*   **Sound (`gui.py` / Pygame):** Integrates with the Pygame library (if available) to load and play `.wav` sound effects triggered by game events.
*   **Main (`main.py`):** The entry point of the application, responsible for importing necessary modules and launching the `TicTacToeGUI`. Includes basic error handling for missing dependencies (like Pygame).

---

## 💻 Code Highlights

### Key Components & Functions

| Component/Function                     | File              | Description                                                       |
| :------------------------------------- | :---------------- | :---------------------------------------------------------------- |
| `TicTacToeGUI` (Class)                 | `gui.py`          | Main class managing the entire GUI application and game flow.     |
| `_setup_ui()`                          | `gui.py`          | Method within `TicTacToeGUI` to create and arrange all widgets.   |
| `apply_theme_to_all()`                 | `gui.py`          | Applies the selected theme's colors to UI elements.             |
| `on_button_click(row, col)`            | `gui.py`          | Handles player clicks on the game grid.                           |
| `ai_move(board, difficulty, symbol)` | `game_logic.py`   | Determines the AI's next move based on the selected difficulty.   |
| `minimax(...)`                         | `game_logic.py`   | Core recursive function for the Minimax algorithm (Hard AI).    |
| `check_winner(board, player)`          | `game_logic.py`   | Checks if the specified player has won the game.                  |
| `get_winning_line(board)`              | `game_logic.py`   | Identifies the coordinates of the winning line for highlighting.  |
| `THEMES` (Dictionary)                  | `themes.py`       | Stores the color definitions for all available visual themes.     |

---

## 📂 Project Structure

    

IGNORE_WHEN_COPYING_START
Use code with caution.Markdown
IGNORE_WHEN_COPYING_END

TICTACTOEGAME/
├── pycache/ # Compiled Python bytecode (auto-generated)
├── sounds/
│ ├── click.wav # Sound for placing a mark
│ ├── lose.wav # Sound for AI winning
│ └── win.wav # Sound for Player winning
├── game_logic.py # Core game rules, state checks, AI algorithms
├── gui.py # Tkinter GUI implementation, event handling, theme application
├── main.py # Main script to launch the application
├── themes.py # Theme color definitions
└── README.md # This file

      
---

## ⚙️ Installation & Setup

1.  **Prerequisites:**
    *   Python 3.x installed.
    *   Tkinter (usually included with Python standard library).
2.  **Clone the Repository (Optional):**
    ```bash
    git clone <your-repository-link>
    cd TICTACTOEGAME
    ```
3.  **Install Dependencies:**
    *   Pygame is required for sound effects. If you want sound, install it:
        ```bash
        pip install pygame
        ```
    *   If you don't need sound, you can run the game, but you might see an error message in the console if Pygame isn't found (the game should still work visually).
4.  **Run the Game:**
    ```bash
    python main.py
    ```

---

## 🙏 Acknowledgments

*(You can add any acknowledgments here if applicable, e.g., course instructors, resources used, etc. If not, you can remove this section.)*

*   *Example: Inspiration from classic Tkinter tutorials.*
*   *Example: Guidance from [Professor/TA Name] if this was for a course.*

---

## 📧 Contact

Let's connect! Feel free to reach out or follow me on these platforms:

[![X (Twitter)](https://img.shields.io/badge/X-black.svg?style=for-the-badge&logo=X&logoColor=white)](https://x.com/abdallasamir04)
[![Facebook](https://img.shields.io/badge/Facebook-1877F2?style=for-the-badge&logo=facebook&logoColor=white)](https://www.facebook.com/abdallasamir04/)
[![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/abdallasamir04)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/abdalla-mahmoud-9264242b6/)
[![Email](https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:samirovic707@gmail.com)
[![GitHub](https://img.shields.io/badge/GitHub-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)](https://github.com/abdallasamir04)

---

**Abdalla Samir**
*(You can add your affiliation here, e.g., University Name, Personal Project, etc.)*

    
