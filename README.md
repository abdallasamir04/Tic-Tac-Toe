# 🎮 Tic-Tac-Toe Game 

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/Language-Python-yellow.svg)
![Tkinter](https://img.shields.io/badge/UI-Tkinter-orange.svg)
![Pygame](https://img.shields.io/badge/Sound-Pygame-lightblue.svg)

**Tic-Tac-Toe Pro GUI** is a classic Tic-Tac-Toe game implemented with a graphical user interface using Python's **Tkinter** library.
It features an intelligent AI opponent with adjustable difficulty levels, multiple visual themes, and optional sound effects (requires **Pygame**).
This project demonstrates GUI development, game logic implementation, and basic AI principles (Minimax). Developed by **_Abdalla Samir_**.

---

## 🚀 Features

*   **Clean GUI:** An intuitive and responsive graphical interface built with Tkinter, featuring a 3x3 game grid and control buttons.
*   **Intelligent AI Opponent:** Play against an AI with three difficulty settings:
    *   `Easy`: Makes random moves.
    *   `Medium`: Basic logic (tries to win, tries to block).
    *   `Hard`: Uses the **Minimax algorithm** with alpha-beta pruning for optimal play.
*   **Multiple Visual Themes:** Choose from **six** different themes (like Sci-Fi, Retro, Forest) to customize the game's appearance.
*   **Optional Sound Effects:** Get audio feedback for button clicks, wins, and losses (requires Pygame installation).
*   **Player Options:** Choose to play as 'X' or 'O' and decide whether to go first or second.
*   **Score Tracking:** Keeps track of wins for the Player, AI, and the number of draws during the current session.
*   **Restart Functionality:** Easily start a new game round without closing the application.

---

## 🛠️ How It Works

1.  **Initialization:** The application starts, sets up the main window, game board grid, control panel, and loads the default theme using `Tkinter`.
2.  **Game Setup:** A setup dialog prompts the player to choose their symbol (X/O) and turn order.
3.  **Player Turn:** The player clicks on an empty cell on the grid. The GUI captures the click event.
4.  **Game Logic Update:** The `gui.py` script updates the internal board representation in `game_logic.py` and visually updates the clicked button.
5.  **State Check:** `game_logic.py` checks if the player's move resulted in a win or a draw.
6.  **AI Turn (if applicable):** If the game continues, `gui.py` calls `game_logic.py`'s `ai_move` function.
7.  **AI Calculation:** Based on the selected difficulty, the AI determines its move (randomly for Easy, basic logic for Medium, Minimax for Hard).
8.  **GUI Update:** The AI's move is reflected on the GUI, and the game state is checked again (AI win or draw).
9.  **Theme Application:** The selected theme's colors are applied to all relevant GUI elements.
10. **Scoring:** Scores are updated after each game ends.

---

## ⚙️ Installation & Running

1.  **Clone the repository:**
    ```bash
    git clone : https://github.com/abdallasamir04/Tic-Tac-Toe.git
    cd TICTACTOEGAME
    ```
2.  **Ensure Python is installed.** (Developed with Python 3.x)
3.  **Install Pygame (for sound effects):**
    ```bash
    pip install pygame
    ```
    *Note: Tkinter usually comes built-in with Python.*
4.  **Run the application:**
    ```bash
    python main.py
    ```

---

## 💻 Code Highlights

### Key Files & Functions

| File / Function                      | Description                                                    |
| ------------------------------------ | -------------------------------------------------------------- |
| **`gui.py`** (`TicTacToeGUI`)        | Manages the main application window, widgets, and event handling. |
| `gui.py` (`__init__`)                | Initializes the GUI elements, game state variables, and theme.   |
| `gui.py` (`_setup_ui`)               | Creates and arranges all the visual components (buttons, labels). |
| `gui.py` (`on_button_click`)         | Handles player clicks on the game grid.                        |
| `gui.py` (`perform_ai_move`)         | Initiates the AI's turn after a delay.                         |
| `gui.py` (`apply_theme_to_all`)      | Applies the selected theme's colors to the GUI.                |
| `gui.py` (`check_game_state`)        | Checks for win/draw conditions after each move & updates UI.   |
| **`game_logic.py`**                  | Contains the core game rules, AI logic, and board checks.      |
| `game_logic.py` (`ai_move`)          | Determines the AI's move based on the chosen difficulty.       |
| `game_logic.py` (`minimax`)          | Implements the Minimax algorithm with alpha-beta pruning (Hard). |
| `game_logic.py` (`check_winner`)     | Checks if a given player has won the game.                     |
| `game_logic.py` (`get_winning_line`) | Returns the coordinates of the winning line, if any.           |
| `game_logic.py` (`init_board`)       | Creates a new, empty game board state.                         |
| **`themes.py`**                      | Defines color dictionaries for different visual themes.        |
| **`main.py`**                        | The main entry point script to launch the `TicTacToeGUI`.      |

---

## 📂 Project Structure :

[TICTACTOEGAME/
│
├── pycache/ # Python bytecode cache (auto-generated)
│
├── sounds/ # Directory for sound files
│ ├── click.wav
│ ├── lose.wav
│ └── win.wav
│
├── game_logic.py # Core game rules, AI logic, board state
├── gui.py # Tkinter GUI implementation, event handling
├── main.py # Main script to run the application
├── README.md # This file
└── themes.py # Theme definitions (colors)

---


## 🙏 Acknowledgments


    Eng. Rahma Yasser - Technical guidance.

    Prof. Mamdouh Farouk - Project supervision.
    
## 📧 Contact

Let's connect! Feel free to reach out or follow me on these platforms:  

[![Facebook](https://img.shields.io/badge/Facebook-1877F2?style=for-the-badge&logo=facebook&logoColor=white)](https://www.facebook.com/abdallasamir04/)  
[![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/abdallasamir04)  
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/abdalla-mahmoud-9264242b6/)  
[![Email](https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:samirovic707@gmail.com)  
[![GitHub](https://img.shields.io/badge/GitHub-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)](https://github.com/abdallasamir04)  
---
**Abdalla Samir**  
**Faculty of Computers and Artificial Intelligence**  
**Assiut National University**  
**Artificial Intelligence Course  - Third Level**
