import tkinter as tk
from tkinter import ttk
import os

try:
    import pygame
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False

import game_logic as gl
from themes import THEMES, DEFAULT_THEME

AI_THINK_DELAY_MS = 400
DIFFICULTY_LEVELS = [gl.EASY, gl.MEDIUM, gl.HARD]
MIN_WINDOW_SIZE = (500, 650)

class TicTacToeGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Tic-Tac-Toe")
        self.window.geometry("500x650")
        self.window.minsize(*MIN_WINDOW_SIZE)
        self.window.resizable(True, True)

        self.player_symbol = None
        self.ai_symbol = None
        self.board = gl.init_board()
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.player_score = 0
        self.ai_score = 0
        self.draw_count = 0
        self.game_active = False
        self.current_difficulty = gl.HARD

        self.sound_enabled = self._init_sound()

        self.themes = THEMES
        self.current_theme_name = DEFAULT_THEME
        self.theme = self.themes[self.current_theme_name]

        self._setup_ui()
        self.apply_theme_to_all()
        self.show_symbol_choice()
        self.window.mainloop()

    def _init_sound(self):
        if not PYGAME_AVAILABLE: return False
        try:
            pygame.mixer.init()
            sounds_dir = "sounds"
            required = ["click.wav", "win.wav", "lose.wav", "draw.wav"]
            if not os.path.isdir(sounds_dir): return False
            if not all(os.path.exists(os.path.join(sounds_dir, s)) for s in required):
                print(f"Warning: Not all sound files found in '{sounds_dir}'. Missing: {[s for s in required if not os.path.exists(os.path.join(sounds_dir, s))]}")
                return False
            return True
        except Exception as e:
            print(f"Sound init error: {e}")
            return False

    def _play_sound(self, sound_name):
        if self.sound_enabled:
            try:
                sound_path = os.path.join("sounds", f"{sound_name}.wav")
                if not os.path.exists(sound_path):
                    print(f"Warning: Sound file not found: {sound_path}")
                    return
                sound = pygame.mixer.Sound(sound_path)
                sound.play()
            except Exception as e:
                print(f"Error playing sound '{sound_name}': {e}")

    def _setup_ui(self):
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_rowconfigure(1, weight=1)

        self.header_frame = tk.Frame(self.window)
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=10)

        self.title_label = tk.Label(
            self.header_frame,
            text="Tic Tac Toe",
            font=("Arial", 20, "bold")
        )
        self.title_label.pack()

        self.dev_label = tk.Label(
            self.header_frame,
            text="Developed By: Abdalla Samir",
            font=("Arial", 13, "bold")
        )
        self.dev_label.pack()

        self.board_frame = tk.Frame(self.window)
        self.board_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)

        for r in range(3):
            self.board_frame.rowconfigure(r, weight=1)
            for c in range(3):
                self.board_frame.columnconfigure(c, weight=1)
                btn = tk.Button(
                    self.board_frame,
                    text=gl.EMPTY,
                    font=("Arial", 36, "bold"),
                    width=3,
                    height=1,
                    relief="flat",
                    command=lambda row=r, col=c: self.on_button_click(row, col)
                )
                btn.grid(row=r, column=c, padx=5, pady=5, sticky="nsew")
                btn.bind("<Enter>", lambda e, row=r, col=c: self.on_hover(row, col, True))
                btn.bind("<Leave>", lambda e, row=r, col=c: self.on_hover(row, col, False))
                self.buttons[r][c] = btn

        self.control_frame = tk.Frame(self.window)
        self.control_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=10)

        for i in range(4):
            self.control_frame.columnconfigure(i, weight=1, uniform="controls")

        self.status_frame = tk.Frame(self.control_frame)
        self.status_frame.grid(row=0, column=0, columnspan=4, sticky="ew", pady=(0, 10))

        self.difficulty_label = tk.Label(
            self.status_frame,
            text=f"Difficulty: {self.current_difficulty}",
            font=("Arial", 12, "bold")
        )
        self.difficulty_label.pack(side=tk.LEFT, expand=True)

        self.turn_label = tk.Label(
            self.status_frame,
            text="Choose X or O to start",
            font=("Arial", 12, "bold")
        )
        self.turn_label.pack(side=tk.LEFT, expand=True)

        self.score_frame = tk.Frame(self.status_frame)
        self.score_frame.pack(side=tk.RIGHT, expand=True)

        self.player_label = tk.Label(
            self.score_frame,
            text=f"Player: {self.player_score}",
            font=("Arial", 12, "bold")
        )
        self.player_label.pack(side=tk.LEFT, padx=5)

        self.draw_label = tk.Label(
            self.score_frame,
            text=f"Draws: {self.draw_count}",
            font=("Arial", 12, "bold")
        )
        self.draw_label.pack(side=tk.LEFT, padx=5)

        self.ai_label = tk.Label(
            self.score_frame,
            text=f"AI: {self.ai_score}",
            font=("Arial", 12, "bold")
        )
        self.ai_label.pack(side=tk.LEFT, padx=5)

        btn_font = ("Arial", 12, "bold")
        btn_pady = 8
        btn_relief = "groove"

        self.restart_btn = tk.Button(
            self.control_frame,
            text="Restart",
            font=btn_font,
            relief=btn_relief,
            command=self.restart_game,
            pady=btn_pady
        )
        self.restart_btn.grid(row=1, column=0, padx=5, sticky="ew")

        self.difficulty_var = tk.StringVar(value=self.current_difficulty)
        self.difficulty_menu = ttk.OptionMenu(
            self.control_frame,
            self.difficulty_var,
            self.current_difficulty,
            *DIFFICULTY_LEVELS,
            command=self.change_difficulty
        )
        self.difficulty_menu.config(width=10)
        self.difficulty_menu.grid(row=1, column=1, padx=5, sticky="ew")

        self.theme_var = tk.StringVar(value=self.current_theme_name)
        self.theme_menu = ttk.OptionMenu(
            self.control_frame,
            self.theme_var,
            self.current_theme_name,
            *self.themes.keys(),
            command=self.change_theme
        )
        self.theme_menu.config(width=10)
        self.theme_menu.grid(row=1, column=2, padx=5, sticky="ew")

        self.exit_btn = tk.Button(
            self.control_frame,
            text="Exit",
            font=btn_font,
            relief=btn_relief,
            command=self.quit_game,
            pady=btn_pady
        )
        self.exit_btn.grid(row=1, column=3, padx=5, sticky="ew")

        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TMenubutton',
                        font=btn_font,
                        relief=btn_relief,
                        padding=(8, btn_pady)
                       )

    def show_symbol_choice(self):
        self.choice_window = tk.Toplevel(self.window)
        self.choice_window.title("Game Setup")
        self.choice_window.resizable(False, False)
        self.choice_window.transient(self.window)
        self.choice_window.grab_set()

        current_theme = self.themes[self.current_theme_name]
        self.choice_window.configure(bg=current_theme["bg"])

        window_width = 500
        window_height = 300
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = int((screen_width/2) - (window_width/2))
        y = int((screen_height/2) - (window_height/2))
        self.choice_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        style = ttk.Style(self.choice_window)
        style.theme_use('clam')

        style.configure('Large.TRadiobutton',
                       background=current_theme["bg"],
                       foreground=current_theme["text"],
                       font=('Arial', 17, 'bold'),
                       selectcolor='blue',
                       indicatorsize=14)

        style.map('Large.TRadiobutton',
                  background=[('selected', current_theme["bg"]),
                              ('active', current_theme.get("hover", current_theme["bg"]))]
                 )

        style.configure('small.TRadiobutton',
                       background=current_theme["bg"],
                       foreground=current_theme["text"],
                       font=('Arial', 15, 'bold'),
                       selectcolor='blue',
                       indicatorsize=14)

        style.map('small.TRadiobutton',
                  background=[('selected', current_theme["bg"]),
                               ('active', current_theme.get("hover", current_theme["bg"]))]
                 )

        symbol_frame = tk.Frame(self.choice_window, bg=current_theme["bg"])
        symbol_frame.pack(pady=(20, 10), fill=tk.X, padx=20)

        tk.Label(
            symbol_frame,
            text="Choose Your Symbol:",
            font=("Arial", 16, "bold"),
            bg=current_theme["bg"],
            fg=current_theme["text"]
        ).pack()

        self.symbol_var = tk.StringVar(value="X")

        symbol_btn_frame = tk.Frame(symbol_frame, bg=current_theme["bg"])
        symbol_btn_frame.pack(pady=10)

        ttk.Radiobutton(
            symbol_btn_frame,
            text="X",
            variable=self.symbol_var,
            value="X",
            style='Large.TRadiobutton'
        ).pack(side=tk.LEFT, padx=20)

        ttk.Radiobutton(
            symbol_btn_frame,
            text="O",
            variable=self.symbol_var,
            value="O",
            style='Large.TRadiobutton'
        ).pack(side=tk.LEFT, padx=20)

        turn_frame = tk.Frame(self.choice_window, bg=current_theme["bg"])
        turn_frame.pack(pady=10, fill=tk.X, padx=20)

        tk.Label(
            turn_frame,
            text="Choose Turn Order:",
            font=("Arial", 16, "bold"),
            bg=current_theme["bg"],
            fg=current_theme["text"]
        ).pack()

        self.turn_var = tk.StringVar(value="first")

        turn_btn_frame = tk.Frame(turn_frame, bg=current_theme["bg"])
        turn_btn_frame.pack(pady=10)

        ttk.Radiobutton(
            turn_btn_frame,
            text="Play First",
            variable=self.turn_var,
            value="first",
            style='small.TRadiobutton'
        ).pack(side=tk.LEFT, padx=20)

        ttk.Radiobutton(
            turn_btn_frame,
            text="Play Second",
            variable=self.turn_var,
            value="second",
            style='small.TRadiobutton'
        ).pack(side=tk.LEFT, padx=20)

        start_btn = tk.Button(
            self.choice_window,
            text="Start Game",
            font=("Arial", 14, "bold"),
            relief="groove",
            bg=current_theme["control_bg"],
            fg=current_theme["control_fg"],
            activebackground=current_theme["control_active"],
            command=self.confirm_symbol_choice,
            width=15,
            pady=5
        )
        start_btn.pack(pady=(15, 20))

        self.window.wait_window(self.choice_window)

    def confirm_symbol_choice(self):
        if self.symbol_var.get() == "X":
            self.player_symbol = gl.PLAYER_X
            self.ai_symbol = gl.AI_O
        else:
            self.player_symbol = gl.AI_O
            self.ai_symbol = gl.PLAYER_X

        self.game_active = True
        self.choice_window.destroy()

        if self.turn_var.get() == "second":
            self.update_status("AI's turn")
            self.window.after(500, self.perform_ai_move)
        else:
            self.update_status("Your turn!")

    def apply_theme_to_all(self):
        self.theme = self.themes[self.current_theme_name]
        bg_color = self.theme["bg"]
        text_color = self.theme["text"]
        player_color = self.theme["player"]
        ai_color = self.theme["ai"]

        self.window.configure(bg=bg_color)
        self.header_frame.configure(bg=bg_color)
        self.board_frame.configure(bg=bg_color)
        self.control_frame.configure(bg=bg_color)
        self.status_frame.configure(bg=bg_color)
        self.score_frame.configure(bg=bg_color)

        self.title_label.configure(bg=bg_color, fg=text_color)
        self.dev_label.configure(bg=bg_color, fg=text_color)
        self.player_label.configure(bg=bg_color, fg=player_color)
        self.draw_label.configure(bg=bg_color, fg=text_color)
        self.ai_label.configure(bg=bg_color, fg=ai_color)
        self.difficulty_label.configure(bg=bg_color, fg=text_color)
        self.turn_label.configure(bg=bg_color, fg=text_color)

        self.restart_btn.configure(
            bg=self.theme["control_bg"],
            fg=self.theme["control_fg"],
            activebackground=self.theme["control_active"]
        )
        self.exit_btn.configure(
            bg=self.theme["exit_bg"],
            fg=self.theme["exit_fg"],
            activebackground=self.theme["exit_active"]
        )

        self.update_button_styles()

    def update_button_styles(self, winning_line=None):
        if winning_line is None:
            winning_line = []

        for r in range(3):
            for c in range(3):
                btn = self.buttons[r][c]
                cell = self.board[r][c]
                is_win = (r, c) in winning_line

                if is_win:
                    btn.configure(
                        bg=self.theme["win"],
                        fg=self.theme["player"] if cell == self.player_symbol else self.theme["ai"],
                        relief="groove"
                    )
                elif cell == self.player_symbol:
                    btn.configure(
                        text=self.player_symbol,
                        fg=self.theme["player"],
                        bg=self.theme["clicked"],
                        state="disabled",
                        relief="sunken"
                    )
                elif cell == self.ai_symbol:
                    btn.configure(
                        text=self.ai_symbol,
                        fg=self.theme["ai"],
                        bg=self.theme["clicked"],
                        state="disabled",
                        relief="sunken"
                    )
                else:
                    btn.configure(
                        text=gl.EMPTY,
                        fg=self.theme["text"],
                        bg=self.theme["btn_bg"],
                        state="normal",
                        relief="flat"
                    )

    def on_hover(self, row, col, is_entering):
        btn = self.buttons[row][col]
        if self.game_active and self.board[row][col] == gl.EMPTY:
            btn.configure(bg=self.theme["hover"] if is_entering else self.theme["btn_bg"])

    def change_difficulty(self, selected_difficulty):
        if selected_difficulty in DIFFICULTY_LEVELS:
            self.current_difficulty = selected_difficulty
            self.difficulty_label.config(text=f"Difficulty: {self.current_difficulty}")
            self.restart_game()

    def change_theme(self, selected_theme_name):
        if selected_theme_name in self.themes:
            self.current_theme_name = selected_theme_name
            self.apply_theme_to_all()

    def update_status(self, message=None):
        if message:
            self.turn_label.config(text=message)
        else:
            if self.player_symbol:
                status = "Your turn!" if self.game_active else "Game over"
                self.turn_label.config(text=status)

    def on_button_click(self, row, col):
        if not self.player_symbol:
            return

        if self.board[row][col] == gl.EMPTY and self.game_active:
            self._play_sound("click")
            self.board[row][col] = self.player_symbol
            self.update_button_styles()

            if self.check_game_state():
                return

            self.update_status("AI thinking...")
            self.window.after(AI_THINK_DELAY_MS, self.perform_ai_move)

    def perform_ai_move(self):
        if not self.game_active:
            return

        move = gl.ai_move(self.board, self.current_difficulty, self.ai_symbol)
        if move:
            row, col = move
            self.board[row][col] = self.ai_symbol
            self.update_button_styles()
            self.check_game_state()
        else:
             self.check_game_state()


    def check_game_state(self):
        winning_line = gl.get_winning_line(self.board)
        if winning_line:
            self.game_active = False
            winner = self.board[winning_line[0][0]][winning_line[0][1]]

            if winner == self.player_symbol:
                self.player_score += 1
                self._play_sound("win")
                status_message = "You win!"
            else:
                self.ai_score += 1
                self._play_sound("lose")
                status_message = "AI wins!"

            self.update_scores()
            self.update_button_styles(winning_line)
            self.update_status(status_message)
            return True

        elif gl.is_board_full(self.board):
            self.game_active = False
            self.draw_count += 1
            self._play_sound("draw")
            self.update_scores()
            self.update_status("It's a draw!")
            self.update_button_styles()
            return True

        return False

    def update_scores(self):
        self.player_label.config(text=f"Player: {self.player_score}")
        self.draw_label.config(text=f"Draws: {self.draw_count}")
        self.ai_label.config(text=f"AI: {self.ai_score}")

    def restart_game(self):
        if not self.player_symbol:
            return

        if self.sound_enabled:
            pygame.mixer.stop()

        self.board = gl.init_board()
        self.game_active = True
        self.update_button_styles()

        if self.player_symbol == gl.AI_O:
            self.update_status("AI's turn")
            self.window.after(500, self.perform_ai_move)
        else:
            self.update_status("Your turn!")

    def quit_game(self):
        if self.sound_enabled:
            pygame.mixer.quit()
        self.window.destroy()
