import tkinter as tk # Import the main tkinter library for creating the GUI
from tkinter import ttk # Import themed tkinter widgets for a more modern look
import os # Import the os module for interacting with the operating system (like checking file paths)

try:
    import pygame # Try to import the pygame library for sound effects
    PYGAME_AVAILABLE = True # Set a flag indicating that pygame was successfully imported
except ImportError:
    PYGAME_AVAILABLE = False # Set a flag indicating that pygame could not be imported

import game_logic as gl # Import the custom game logic module (contains board checks, AI logic, constants like EMPTY, PLAYER_X, AI_O, EASY, MEDIUM, HARD)
from themes import THEMES, DEFAULT_THEME # Import theme definitions (dictionary) and the default theme name from a custom themes module

# Constants
AI_THINK_DELAY_MS = 400 # Delay in milliseconds before the AI makes its move (to simulate thinking)
DIFFICULTY_LEVELS = [gl.EASY, gl.MEDIUM, gl.HARD] # List of available difficulty levels, using constants defined in game_logic
MIN_WINDOW_SIZE = (500, 650) # Minimum allowed size (width, height) for the main application window

class TicTacToeGUI: # Defines the main class for the Tic-Tac-Toe application GUI
    def __init__(self): # Constructor for the TicTacToeGUI class, initializes the application
        self.window = tk.Tk() # Create the main application window instance
        self.window.title("Tic-Tac-Toe") # Set the text that appears in the window's title bar
        self.window.geometry("500x650") # Set the initial width and height of the window
        self.window.minsize(*MIN_WINDOW_SIZE) # Set the minimum allowed size using the MIN_WINDOW_SIZE constant (* unpacks the tuple)
        self.window.resizable(True, True) # Allow the window to be resized both horizontally and vertically

        # Game State - Initialize variables to store the current state of the game
        self.player_symbol = None # Symbol ('X' or 'O') chosen by the player (will be set later during setup)
        self.ai_symbol = None # Symbol ('X' or 'O') for the AI (will be the opposite of the player's symbol)
        self.board = gl.init_board() # Initialize the game board (likely a 3x3 list of lists) using a function from game_logic
        self.buttons = [[None for _ in range(3)] for _ in range(3)] # Create a 2D list (3x3) to hold the tkinter Button widgets for the grid cells
        self.player_score = 0 # Initialize the player's score counter
        self.ai_score = 0 # Initialize the AI's score counter
        self.draw_count = 0 # Initialize the counter for draw games
        self.game_active = False # Flag to track if a game is currently in progress (starts as False until setup is complete)
        self.current_difficulty = gl.HARD # Set the default AI difficulty level using the constant from game_logic

        # Sound - Initialize sound-related attributes
        self.sound_enabled = self._init_sound() # Call the internal method to check if sound can be initialized and set a boolean flag

        # Themes - Initialize theme-related attributes
        self.themes = THEMES # Store the dictionary of available themes (loaded from the themes module)
        self.current_theme_name = DEFAULT_THEME # Set the name of the initially active theme using the constant from themes module
        self.theme = self.themes[self.current_theme_name] # Get the actual theme settings dictionary for the current theme

        # UI Setup - Set up the user interface elements
        self._setup_ui() # Call the internal method to create and arrange all the visual widgets
        self.apply_theme_to_all() # Apply the colors and styles from the initial theme to all relevant widgets
        self.show_symbol_choice() # Display the pop-up window for the user to choose their symbol (X/O) and turn order
        self.window.mainloop() # Start the tkinter event loop, which makes the window interactive and waits for user input

    def _init_sound(self): # Internal method to initialize the sound system using pygame
        if not PYGAME_AVAILABLE: return False # If pygame failed to import earlier, immediately return False (sound not available)
        try:
            pygame.mixer.init() # Initialize the pygame mixer module
            sounds_dir = "sounds" # Define the name of the directory where sound files are expected
            # Make sure "draw.wav" is included in the list of required files
            required = ["click.wav", "win.wav", "lose.wav", "draw.wav"] # <--- MODIFIED
            if not os.path.isdir(sounds_dir): return False # Check if the 'sounds' directory exists; if not, return False
            # Check if all required sound files exist within the 'sounds' directory
            if not all(os.path.exists(os.path.join(sounds_dir, s)) for s in required):
                print(f"Warning: Not all sound files found in '{sounds_dir}'. Missing: {[s for s in required if not os.path.exists(os.path.join(sounds_dir, s))]}") # Optional: More specific warning
                return False
            return True # If initialization and all file checks pass, return True (sound is enabled)
        except Exception as e: # Catch any potential errors during pygame mixer initialization or file checks
            print(f"Sound init error: {e}") # Print an error message to the console
            return False # Return False indicating sound initialization failed

    def _play_sound(self, sound_name): # Internal method to play a specific sound file
        if self.sound_enabled: # Only attempt to play sound if the sound system was successfully initialized
            try:
                sound_path = os.path.join("sounds", f"{sound_name}.wav") # Construct the full path to the requested sound file (e.g., "sounds/click.wav")
                # Check if the specific sound file exists before trying to load it
                if not os.path.exists(sound_path):
                    print(f"Warning: Sound file not found: {sound_path}")
                    return
                sound = pygame.mixer.Sound(sound_path) # Load the sound file into a pygame Sound object
                sound.play() # Play the loaded sound effect
            except Exception as e: # Catch any errors during sound loading or playing
                print(f"Error playing sound '{sound_name}': {e}") # Print an error message to the console

    def _setup_ui(self): # Internal method to create and arrange all the GUI widgets
        # Configure main grid - Control how the main window's rows and columns resize
        self.window.grid_columnconfigure(0, weight=1) # Allow the first (and only) column to expand horizontally if the window is resized
        self.window.grid_rowconfigure(1, weight=1) # Allow the second row (where the board frame will be) to expand vertically

        # Header Frame - Create a frame at the top for the title and developer credit
        self.header_frame = tk.Frame(self.window) # Initialize the Frame widget, placing it inside the main window
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=10) # Place the frame in the grid (row 0, col 0), make it stretch horizontally ("ew"), add padding

        # Create the main title label
        self.title_label = tk.Label(
            self.header_frame, # Place this label inside the header frame
            text="Tic Tac Toe", # Set the text content
            font=("Arial", 20, "bold") # Set the font family, size, and style
        )
        self.title_label.pack() # Add the title label to the header frame using the pack geometry manager (centers it by default)

        # Create the developer credit label
        self.dev_label = tk.Label(
            self.header_frame, # Place this label inside the header frame
            text="Developed By: Abdalla Samir", # Set the text content
            font=("Arial", 13, "bold") # Set the font
        )
        self.dev_label.pack() # Add the developer label below the title label in the header frame

        # Board Frame - Create a frame in the middle to hold the 3x3 game grid buttons
        self.board_frame = tk.Frame(self.window) # Initialize the Frame widget, placing it inside the main window
        self.board_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10) # Place the frame in the grid (row 1, col 0), make it stretch in all directions ("nsew"), add padding

        # Create the 3x3 grid of buttons
        for r in range(3): # Loop through the rows (0, 1, 2)
            self.board_frame.rowconfigure(r, weight=1) # Allow each row within the board frame to expand vertically
            for c in range(3): # Loop through the columns (0, 1, 2)
                self.board_frame.columnconfigure(c, weight=1) # Allow each column within the board frame to expand horizontally
                # Create a button for the current cell (r, c)
                btn = tk.Button(
                    self.board_frame, # Place this button inside the board frame
                    text=gl.EMPTY, # Initial text is the empty symbol (likely ' ') from game_logic
                    font=("Arial", 36, "bold"), # Set a large, bold font for 'X' and 'O'
                    width=3, # Set a fixed width (in text units)
                    height=1, # Set a fixed height (in text units)
                    relief="flat", # Set the border style to flat initially
                    # Set the command to call on_button_click, passing the specific row and col using lambda
                    command=lambda row=r, col=c: self.on_button_click(row, col)
                )
                # Place the button in the board frame's grid at the current row and column
                # Make it stretch to fill its cell ("nsew"), add small padding around it
                btn.grid(row=r, column=c, padx=5, pady=5, sticky="nsew")
                # Bind the mouse entering event (<Enter>) to the on_hover method (passing row, col, and True for entering)
                btn.bind("<Enter>", lambda e, row=r, col=c: self.on_hover(row, col, True))
                # Bind the mouse leaving event (<Leave>) to the on_hover method (passing row, col, and False for leaving)
                btn.bind("<Leave>", lambda e, row=r, col=c: self.on_hover(row, col, False))
                self.buttons[r][c] = btn # Store the created button widget in our 2D list for later access

        # Control Frame - Create a frame at the bottom for control elements (status, scores, buttons)
        self.control_frame = tk.Frame(self.window) # Initialize the Frame widget, placing it inside the main window
        self.control_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=10) # Place the frame in the grid (row 2, col 0), make it stretch horizontally, add padding

        # Configure columns within the control frame to distribute space evenly for the buttons below
        for i in range(4): # There will be 4 controls in the bottom row (Restart, Difficulty, Theme, Exit)
            # weight=1 makes columns expandable, uniform="controls" makes them share space equally
            self.control_frame.columnconfigure(i, weight=1, uniform="controls")

        # Status Frame - Create a frame within the control frame to hold status information (Difficulty, Turn/Status, Score)
        self.status_frame = tk.Frame(self.control_frame) # Initialize the Frame, placing it inside the control frame
        # Place the status frame in the control frame's grid (row 0), make it span all 4 columns, stretch horizontally, add bottom padding
        self.status_frame.grid(row=0, column=0, columnspan=4, sticky="ew", pady=(0, 10))

        # Create the label to display the current difficulty level
        self.difficulty_label = tk.Label(
            self.status_frame, # Place this label inside the status frame
            text=f"Difficulty: {self.current_difficulty}", # Initial text showing the default difficulty
            font=("Arial", 12, "bold") # Set the font
        )
        # Add the difficulty label to the status frame using pack, allowing it to expand and take available space on the left
        self.difficulty_label.pack(side=tk.LEFT, expand=True)

        # Create the label to display whose turn it is or the game result
        self.turn_label = tk.Label(
            self.status_frame, # Place this label inside the status frame
            text="Choose X or O to start", # Initial message before the game starts
            font=("Arial", 12, "bold") # Set the font
        )
        # Add the turn label to the status frame, packing it to the left (after difficulty label), allowing it to expand
        self.turn_label.pack(side=tk.LEFT, expand=True)

        # Score Frame - Create a sub-frame within the status frame specifically for the score labels
        self.score_frame = tk.Frame(self.status_frame) # Initialize the Frame, placing it inside the status frame
        # Add the score frame to the status frame, packing it to the right, allowing it to expand
        self.score_frame.pack(side=tk.RIGHT, expand=True)

        # Create the label for the player's score
        self.player_label = tk.Label(
            self.score_frame, # Place this label inside the score frame
            text=f"Player: {self.player_score}", # Initial text showing player score (0)
            font=("Arial", 12, "bold") # Set the font
        )
        # Add the player score label to the score frame, packing it to the left, with horizontal padding
        self.player_label.pack(side=tk.LEFT, padx=5)

        # Create the label for the draw count
        self.draw_label = tk.Label(
            self.score_frame, # Place this label inside the score frame
            text=f"Draws: {self.draw_count}", # Initial text showing draw count (0)
            font=("Arial", 12, "bold") # Set the font
        )
        # Add the draw label to the score frame, packing it to the left (after player score), with horizontal padding
        self.draw_label.pack(side=tk.LEFT, padx=5)

        # Create the label for the AI's score
        self.ai_label = tk.Label(
            self.score_frame, # Place this label inside the score frame
            text=f"AI: {self.ai_score}", # Initial text showing AI score (0)
            font=("Arial", 12, "bold") # Set the font
        )
        # Add the AI score label to the score frame, packing it to the left (after draw count), with horizontal padding
        self.ai_label.pack(side=tk.LEFT, padx=5)

        # Control buttons - Define styles and create the main control buttons below the status info
        btn_font = ("Arial", 12, "bold") # Define a common font for the control buttons
        btn_pady = 8 # Define vertical padding for the control buttons
        btn_relief = "groove" # Define a common border style for the control buttons

        # Create the Restart button
        self.restart_btn = tk.Button(
            self.control_frame, # Place this button inside the control frame
            text="Restart", # Set button text
            font=btn_font, # Use the defined button font
            relief=btn_relief, # Use the defined button relief style
            command=self.restart_game, # Set the function to call when this button is clicked
            pady=btn_pady # Apply the defined vertical padding
        )
        # Place the Restart button in the control frame's grid (row 1, col 0), make it stretch horizontally, add horizontal padding
        self.restart_btn.grid(row=1, column=0, padx=5, sticky="ew")

        # Create a tkinter string variable to hold the currently selected difficulty
        self.difficulty_var = tk.StringVar(value=self.current_difficulty)
        # Create a themed OptionMenu (dropdown) for selecting the difficulty
        self.difficulty_menu = ttk.OptionMenu(
            self.control_frame, # Place this dropdown inside the control frame
            self.difficulty_var, # Link it to the difficulty string variable
            self.current_difficulty, # Set the initial displayed value
            *DIFFICULTY_LEVELS, # Provide the list of available options (* unpacks the list)
            command=self.change_difficulty # Set the function to call when an option is selected
        )
        self.difficulty_menu.config(width=10) # Set a fixed width for the dropdown widget
        # Place the difficulty dropdown in the control frame's grid (row 1, col 1), make it stretch horizontally, add padding
        self.difficulty_menu.grid(row=1, column=1, padx=5, sticky="ew")

        # Create a tkinter string variable to hold the currently selected theme name
        self.theme_var = tk.StringVar(value=self.current_theme_name)
        # Create a themed OptionMenu (dropdown) for selecting the theme
        self.theme_menu = ttk.OptionMenu(
            self.control_frame, # Place this dropdown inside the control frame
            self.theme_var, # Link it to the theme string variable
            self.current_theme_name, # Set the initial displayed value
            *self.themes.keys(), # Provide the list of available theme names (* unpacks the dictionary keys)
            command=self.change_theme # Set the function to call when a theme is selected
        )
        self.theme_menu.config(width=10) # Set a fixed width for the dropdown widget
        # Place the theme dropdown in the control frame's grid (row 1, col 2), make it stretch horizontally, add padding
        self.theme_menu.grid(row=1, column=2, padx=5, sticky="ew")

        # Create the Exit button
        self.exit_btn = tk.Button(
            self.control_frame, # Place this button inside the control frame
            text="Exit", # Set button text
            font=btn_font, # Use the defined button font
            relief=btn_relief, # Use the defined button relief style
            command=self.quit_game, # Set the function to call when this button is clicked
            pady=btn_pady # Apply the defined vertical padding
        )
        # Place the Exit button in the control frame's grid (row 1, col 3), make it stretch horizontally, add padding
        self.exit_btn.grid(row=1, column=3, padx=5, sticky="ew")

        # Style the ttk OptionMenu widgets to look more like the standard Buttons
        style = ttk.Style() # Get the ttk styling object
        style.theme_use('clam') # Set the base theme for ttk widgets (influences OptionMenu appearance)
        # Configure the 'TMenubutton' style (which OptionMenu uses)
        style.configure('TMenubutton',
                        font=btn_font, # Apply the same font as standard buttons
                        relief=btn_relief, # Apply the same relief style (may not work perfectly depending on theme)
                        padding=(8, btn_pady) # Apply horizontal (arbitrary 8) and vertical padding (using btn_pady)
                       )

    def show_symbol_choice(self): # Method to display the initial game setup dialog (Toplevel window)
        self.choice_window = tk.Toplevel(self.window) # Create a new Toplevel window (a separate pop-up window)
        self.choice_window.title("Game Setup") # Set the title for the dialog window
        self.choice_window.resizable(False, False) # Prevent the user from resizing this dialog
        self.choice_window.transient(self.window) # Link the dialog to the main window (e.g., it stays on top)
        self.choice_window.grab_set() # Make the dialog modal - user must interact with this window before returning to the main window

        current_theme = self.themes[self.current_theme_name] # Get the settings dictionary for the currently active theme
        self.choice_window.configure(bg=current_theme["bg"]) # Set the background color of the dialog window based on the theme

        # Center the dialog window on the screen
        window_width = 500 # Desired width of the dialog
        window_height = 300 # Desired height of the dialog
        screen_width = self.window.winfo_screenwidth() # Get the screen width
        screen_height = self.window.winfo_screenheight() # Get the screen height
        # Calculate the x and y coordinates for the top-left corner of the dialog
        x = int((screen_width/2) - (window_width/2))
        y = int((screen_height/2) - (window_height/2))
        self.choice_window.geometry(f"{window_width}x{window_height}+{x}+{y}") # Set the size and position of the dialog

        # --- Style Definitions --- Section for defining ttk styles specific to the choice window's widgets
        style = ttk.Style(self.choice_window) # Create a style object associated with the choice window
        style.theme_use('clam') # Ensure the 'clam' theme is used as the base for styling ttk widgets here

        # --- Style for X/O buttons (Large indicator) --- Configure a custom style for the X/O symbol choice Radiobuttons
        style.configure('Large.TRadiobutton', # Define a new style named 'Large.TRadiobutton'
                       background=current_theme["bg"], # Set background color from the theme
                       foreground=current_theme["text"], # Set text color from the theme
                       font=('Arial', 17, 'bold'), # Set the font for the "X" / "O" text next to the radio button
                       selectcolor='blue',  # Set the color of the radio button indicator itself when selected (a blue circle)
                       indicatorsize=14) # Set the size of the circular indicator

        # --- CHANGE 1: Add map to prevent background change on selection ---
        # Map style properties for different states to override default behavior (like background changing on select)
        style.map('Large.TRadiobutton', # Target the 'Large.TRadiobutton' style
                  # Keep the background the same color ('bg' from theme) even when the radio button is 'selected'
                  background=[('selected', current_theme["bg"]),
                              # Optionally, set a hover background color if 'hover' is defined in the theme, otherwise keep it 'bg'
                              ('active', current_theme.get("hover", current_theme["bg"]))]
                 )
        # --- End Change 1 ---

        # --- Style for Play First/Second buttons (Larger text) --- Configure a custom style for the turn choice Radiobuttons
        style.configure('small.TRadiobutton', # Define a new style named 'small.TRadiobutton'
                       background=current_theme["bg"], # Match background color from the theme
                       foreground=current_theme["text"], # Match text color from the theme
                       font=('Arial', 15, 'bold'), # Set a slightly smaller but still large font for "Play First"/"Play Second"
                       selectcolor='blue', # Keep the indicator color consistent
                       indicatorsize=14) # Keep the indicator size consistent

        # --- CHANGE 2: Add map to prevent background change on selection ---
        # Map style properties for the 'small.TRadiobutton' style
        style.map('small.TRadiobutton', # Target the 'small.TRadiobutton' style
                  # Keep the background the same color ('bg' from theme) when 'selected'
                  background=[('selected', current_theme["bg"]),
                               # Optionally, set a hover background color
                               ('active', current_theme.get("hover", current_theme["bg"]))]
                 )
        # --- End Change 2 ---

        # Symbol Selection - Create widgets for choosing the player's symbol (X or O)
        symbol_frame = tk.Frame(self.choice_window, bg=current_theme["bg"]) # Create a frame for symbol selection elements, themed background
        symbol_frame.pack(pady=(20, 10), fill=tk.X, padx=20) # Add frame to window, add padding, make it fill horizontally

        # Create the label "Choose Your Symbol:"
        tk.Label(
            symbol_frame, # Place inside symbol frame
            text="Choose Your Symbol:",
            font=("Arial", 16, "bold"),
            bg=current_theme["bg"], # Themed background
            fg=current_theme["text"] # Themed text color
        ).pack() # Add the label to the frame

        # Create a tkinter string variable to store the chosen symbol ('X' or 'O'), default to 'X'
        self.symbol_var = tk.StringVar(value="X")

        # Create a sub-frame to hold the 'X' and 'O' radio buttons side-by-side
        symbol_btn_frame = tk.Frame(symbol_frame, bg=current_theme["bg"]) # Themed background
        symbol_btn_frame.pack(pady=10) # Add this frame below the label, add vertical padding

        # Create the 'X' radio button using the themed ttk.Radiobutton
        ttk.Radiobutton(
            symbol_btn_frame, # Place inside the button frame
            text="X", # Text displayed next to the button
            variable=self.symbol_var, # Link this button to the symbol variable
            value="X", # This button represents the value 'X'
            style='Large.TRadiobutton' # Apply the custom 'Large' style defined earlier
        ).pack(side=tk.LEFT, padx=20) # Add the button, place it to the left, add horizontal padding

        # Create the 'O' radio button
        ttk.Radiobutton(
            symbol_btn_frame, # Place inside the button frame
            text="O", # Text displayed
            variable=self.symbol_var, # Link to the same variable
            value="O", # This button represents the value 'O'
            style='Large.TRadiobutton' # Apply the same custom 'Large' style
        ).pack(side=tk.LEFT, padx=20) # Add the button to the left of the 'X' button, add padding

        # Turn Selection - Create widgets for choosing whether the player plays first or second
        turn_frame = tk.Frame(self.choice_window, bg=current_theme["bg"]) # Create a frame for turn selection elements
        turn_frame.pack(pady=10, fill=tk.X, padx=20) # Add frame below symbol selection, add padding, fill horizontally

        # Create the label "Choose Turn Order:"
        tk.Label(
            turn_frame, # Place inside turn frame
            text="Choose Turn Order:",
            font=("Arial", 16, "bold"),
            bg=current_theme["bg"], # Themed background
            fg=current_theme["text"] # Themed text color
        ).pack() # Add the label to the frame

        # Create a tkinter string variable to store the chosen turn ('first' or 'second'), default to 'first'
        self.turn_var = tk.StringVar(value="first")

        # Create a sub-frame to hold the 'Play First' and 'Play Second' radio buttons
        turn_btn_frame = tk.Frame(turn_frame, bg=current_theme["bg"]) # Themed background
        turn_btn_frame.pack(pady=10) # Add this frame below the label, add padding

        # Create the 'Play First' radio button
        ttk.Radiobutton(
            turn_btn_frame, # Place inside the turn button frame
            text="Play First", # Text displayed
            variable=self.turn_var, # Link to the turn variable
            value="first", # This button represents the value 'first'
            style='small.TRadiobutton' # Apply the custom 'small' style defined earlier
        ).pack(side=tk.LEFT, padx=20) # Add button to the left, add padding

        # Create the 'Play Second' radio button
        ttk.Radiobutton(
            turn_btn_frame, # Place inside the turn button frame
            text="Play Second", # Text displayed
            variable=self.turn_var, # Link to the same variable
            value="second", # This button represents the value 'second'
            style='small.TRadiobutton' # Apply the same custom 'small' style
        ).pack(side=tk.LEFT, padx=20) # Add button to the left of 'Play First', add padding

        # Start Button - Create the button to confirm choices and start the actual game
        start_btn = tk.Button(
            self.choice_window, # Place button directly in the choice window
            text="Start Game", # Button text
            font=("Arial", 14, "bold"), # Button font
            relief="groove", # Button border style
            bg=current_theme["control_bg"], # Background color from theme's control button settings
            fg=current_theme["control_fg"], # Text color from theme's control button settings
            activebackground=current_theme["control_active"], # Background color when clicked, from theme
            command=self.confirm_symbol_choice, # Set the function to call when this button is clicked
            width=15, # Set button width
            pady=5 # Add vertical padding inside the button
        )
        start_btn.pack(pady=(15, 20)) # Add the button to the window, add vertical padding above and below

        # Pause execution of the __init__ method until the choice window is closed (either by button or 'X')
        self.window.wait_window(self.choice_window)

    def confirm_symbol_choice(self): # Method called when the 'Start Game' button in the dialog is clicked
        # Set player and AI symbols based on the radio button selection in the dialog
        if self.symbol_var.get() == "X": # If the player chose 'X'
            self.player_symbol = gl.PLAYER_X # Assign the player 'X' (using constant from game_logic)
            self.ai_symbol = gl.AI_O # Assign the AI 'O' (using constant from game_logic)
        else: # If the player chose 'O'
            self.player_symbol = gl.AI_O # Assign the player 'O'
            self.ai_symbol = gl.PLAYER_X # Assign the AI 'X'

        # Start the game - Update game state now that settings are confirmed
        self.game_active = True # Mark the game as active, allowing interactions with the board
        self.choice_window.destroy() # Close the symbol choice dialog window

        # Set initial turn based on the turn selection radio buttons
        if self.turn_var.get() == "second": # If the player chose to play second
            self.update_status("AI's turn") # Update the status label on the main window
            # Schedule the AI's first move to happen after a short delay (500ms)
            # This gives the player a moment to see the board before the AI plays
            self.window.after(500, self.perform_ai_move)
        else: # If the player chose to play first
            self.update_status("Your turn!") # Update the status label indicating it's the player's turn

    def apply_theme_to_all(self): # Method to apply the selected theme's colors and styles to all relevant UI elements
        self.theme = self.themes[self.current_theme_name] # Get the dictionary of settings for the currently selected theme name
        # Extract specific color values from the theme dictionary for easier use
        bg_color = self.theme["bg"] # Background color
        text_color = self.theme["text"] # General text color
        player_color = self.theme["player"] # Color for the player's symbol/score
        ai_color = self.theme["ai"] # Color for the AI's symbol/score

        # Apply colors to the main window and major frames
        self.window.configure(bg=bg_color)
        self.header_frame.configure(bg=bg_color)
        self.board_frame.configure(bg=bg_color)
        self.control_frame.configure(bg=bg_color)
        self.status_frame.configure(bg=bg_color)
        self.score_frame.configure(bg=bg_color)

        # Apply colors to labels
        self.title_label.configure(bg=bg_color, fg=text_color)
        self.dev_label.configure(bg=bg_color, fg=text_color)
        self.player_label.configure(bg=bg_color, fg=player_color) # Use specific player color
        self.draw_label.configure(bg=bg_color, fg=text_color)
        self.ai_label.configure(bg=bg_color, fg=ai_color) # Use specific AI color
        self.difficulty_label.configure(bg=bg_color, fg=text_color)
        self.turn_label.configure(bg=bg_color, fg=text_color)

        # Apply specific theme colors to control buttons (Restart, Exit)
        self.restart_btn.configure(
            bg=self.theme["control_bg"], # Background for regular control buttons
            fg=self.theme["control_fg"], # Foreground for regular control buttons
            activebackground=self.theme["control_active"] # Background when clicked
        )
        self.exit_btn.configure(
            bg=self.theme["exit_bg"], # Background for the exit button (can be different)
            fg=self.theme["exit_fg"], # Foreground for the exit button
            activebackground=self.theme["exit_active"] # Background when clicked for exit button
        )

        # Apply theme styles to the grid buttons (needs to consider current board state)
        self.update_button_styles() # Call the method that handles grid button appearance

    def update_button_styles(self, winning_line=None): # Method to update the appearance (text, color, state) of the 3x3 grid buttons
        # Initialize winning_line as an empty list if it wasn't passed (e.g., during theme change or normal play)
        if winning_line is None:
            winning_line = []

        # Loop through each button in the 3x3 grid
        for r in range(3):
            for c in range(3):
                btn = self.buttons[r][c] # Get the Button widget at (r, c)
                cell = self.board[r][c] # Get the state of the corresponding cell from the internal board (' ', 'X', 'O')
                is_win = (r, c) in winning_line # Check if this specific button's coordinates are in the winning line list

                if is_win: # If this button is part of the winning line
                    # Apply winning style: highlight background, use player/AI color for text, sunken relief
                    btn.configure(
                        bg=self.theme["win"], # Use the special 'win' background color from the theme
                        # Set text color based on who won (player or AI)
                        fg=self.theme["player"] if cell == self.player_symbol else self.theme["ai"],
                        relief="groove" # Use a distinct relief style for winning cells
                    )
                elif cell == self.player_symbol: # If the cell contains the player's symbol (and is not winning)
                    # Apply player's move style: show symbol, use player color, use 'clicked' background, disable button, sunken relief
                    btn.configure(
                        text=self.player_symbol, # Display the player's symbol ('X' or 'O')
                        fg=self.theme["player"], # Use the player's color from the theme
                        bg=self.theme["clicked"], # Use the 'clicked' background color from the theme
                        state="disabled", # Disable the button so it can't be clicked again
                        relief="sunken" # Use sunken relief to indicate it's pressed/used
                    )
                elif cell == self.ai_symbol: # If the cell contains the AI's symbol (and is not winning)
                    # Apply AI's move style: show symbol, use AI color, use 'clicked' background, disable button, sunken relief
                    btn.configure(
                        text=self.ai_symbol, # Display the AI's symbol ('X' or 'O')
                        fg=self.theme["ai"], # Use the AI's color from the theme
                        bg=self.theme["clicked"], # Use the 'clicked' background color
                        state="disabled", # Disable the button
                        relief="sunken" # Use sunken relief
                    )
                else: # If the cell is empty (gl.EMPTY)
                    # Apply default empty style: clear text, use default text color (though invisible), use button background, enable button, flat relief
                    btn.configure(
                        text=gl.EMPTY, # Set text to empty (space)
                        fg=self.theme["text"], # Use the general text color (though text is empty)
                        bg=self.theme["btn_bg"], # Use the default button background color from the theme
                        state="normal", # Ensure the button is enabled for clicking
                        relief="flat" # Use flat relief for empty, clickable buttons
                    )

    def on_hover(self, row, col, is_entering): # Method called when the mouse cursor enters or leaves a grid button
        btn = self.buttons[row][col] # Get the Button widget at (row, col)
        # Only change appearance if the game is active and the button corresponds to an empty cell
        if self.game_active and self.board[row][col] == gl.EMPTY:
            # If the mouse is entering, set background to the 'hover' color from the theme
            # If the mouse is leaving, set background back to the default 'btn_bg' color
            btn.configure(bg=self.theme["hover"] if is_entering else self.theme["btn_bg"])

    def change_difficulty(self, selected_difficulty): # Method called when a new difficulty is selected from the dropdown menu
        if selected_difficulty in DIFFICULTY_LEVELS: # Check if the selected value is one of the valid difficulty levels
            self.current_difficulty = selected_difficulty # Update the game's current difficulty setting
            self.difficulty_label.config(text=f"Difficulty: {self.current_difficulty}") # Update the text of the difficulty label
            self.restart_game() # Restart the game immediately with the new difficulty setting

    def change_theme(self, selected_theme_name): # Method called when a new theme is selected from the dropdown menu
        if selected_theme_name in self.themes: # Check if the selected theme name exists in our themes dictionary
            self.current_theme_name = selected_theme_name # Update the game's current theme name
            self.apply_theme_to_all() # Apply the colors and styles of the newly selected theme to the entire UI

    def update_status(self, message=None): # Method to update the text of the turn/status label
        if message: # If a specific message string is provided
            self.turn_label.config(text=message) # Set the label text directly to that message
        else: # If no specific message is provided, determine the status automatically
            # This part seems slightly off, as player_symbol might be None initially.
            # It's generally called with a specific message or after game state checks.
            if self.player_symbol: # Ensure player symbol is set before trying to determine turns (should be true after setup)
                # Determine status based on whether the game is currently active
                status = "Your turn!" if self.game_active else "Game over" # Simplified status (actual turn logic is handled elsewhere)
                self.turn_label.config(text=status) # Update the label text

    def on_button_click(self, row, col): # Method called when a player clicks on one of the 3x3 grid buttons
        if not self.player_symbol: # If symbols haven't been assigned yet (game setup not complete)
            return # Do nothing

        # Check if the clicked cell is currently empty and if the game is active (not ended)
        if self.board[row][col] == gl.EMPTY and self.game_active:
            self._play_sound("click") # Play the 'click' sound effect
            self.board[row][col] = self.player_symbol # Update the internal game board state with the player's symbol
            self.update_button_styles() # Update the appearance of the clicked button (show symbol, disable, change color)

            # Check if the player's move ended the game (win or draw)
            if self.check_game_state():
                return # If the game ended, stop further actions for this turn

            # If the game didn't end, it's the AI's turn
            self.update_status("AI thinking...") # Update the status label
            # Schedule the AI's move to be performed after the AI_THINK_DELAY_MS delay
            self.window.after(AI_THINK_DELAY_MS, self.perform_ai_move)

    def perform_ai_move(self): # Method to execute the AI's turn
        if not self.game_active: # Double-check if the game is still active (it might have ended just before this was called)
            return # If not active, do nothing

        # Get the AI's chosen move (row, col tuple) by calling the ai_move function from game_logic
        # Pass the current board, difficulty level, and the AI's symbol
        move = gl.ai_move(self.board, self.current_difficulty, self.ai_symbol)
        if move: # If ai_move returned a valid move (it should unless the board is full and somehow game_active is still true)
            row, col = move # Unpack the row and column from the returned tuple
            self.board[row][col] = self.ai_symbol # Update the internal game board state with the AI's symbol
            self.update_button_styles() # Update the appearance of the button corresponding to the AI's move
            self.check_game_state() # Check if the AI's move ended the game (win or draw)
        else:
             # This case should ideally not happen if check_game_state is called correctly after player moves.
             # If it does, likely means board is full but wasn't detected as draw previously.
             self.check_game_state() # Re-check state just in case.


    def check_game_state(self): # Method to check if the current board state represents a win, loss, or draw
        winning_line = gl.get_winning_line(self.board) # Call game_logic function to check for a winning line; returns list of winning coords or None
        if winning_line: # If a winning line was found
            self.game_active = False # Mark the game as no longer active
            # Determine the winner ('X' or 'O') by looking at the symbol in the first cell of the winning line
            winner = self.board[winning_line[0][0]][winning_line[0][1]]

            if winner == self.player_symbol: # If the winner's symbol matches the player's symbol
                self.player_score += 1 # Increment the player's score
                self._play_sound("win") # Play the winning sound effect
                status_message = "You win!" # Set status message for player win
            else: # If the winner's symbol matches the AI's symbol
                self.ai_score += 1 # Increment the AI's score
                self._play_sound("lose") # Play the losing sound effect
                status_message = "AI wins!" # Set status message for AI win

            self.update_scores() # Update the score display labels on the UI
            self.update_button_styles(winning_line) # Update the grid buttons, passing the winning line to highlight it
            self.update_status(status_message) # Update the status label with the win/loss message
            return True # Return True indicating that the game has ended

        elif gl.is_board_full(self.board): # If there was no winner, check if the board is full (using game_logic function)
            self.game_active = False # Mark the game as no longer active
            self.draw_count += 1 # Increment the draw counter
            self._play_sound("draw") # <--- ADDED: Play draw sound here
            self.update_scores() # Update the score display labels
            self.update_status("It's a draw!") # Update the status label to indicate a draw
            # No winning line to highlight, so just update button styles normally (disables remaining if any)
            self.update_button_styles()
            return True # Return True indicating that the game has ended

        # If the game did not end, return False
        return False

    def update_scores(self): # Method to update the text of the score labels on the UI
        self.player_label.config(text=f"Player: {self.player_score}") # Update player score label text
        self.draw_label.config(text=f"Draws: {self.draw_count}") # Update draw count label text
        self.ai_label.config(text=f"AI: {self.ai_score}") # Update AI score label text

    def restart_game(self): # Method to reset the game board for a new round
        if not self.player_symbol: # Prevent restarting if the initial setup (symbol choice) hasn't happened
            return # Do nothing

        if self.sound_enabled: # If sound is enabled
            pygame.mixer.stop() # Stop any currently playing sound effects (like win/lose sounds)

        self.board = gl.init_board() # Reset the internal game board state to an empty 3x3 grid
        self.game_active = True # Mark the new game as active
        self.update_button_styles() # Reset the appearance of all grid buttons (make them empty, enabled, default colors)

        # Determine who starts the new game based on the original choice
        # If player chose 'O', AI ('X') starts. If player chose 'X', player starts.
        if self.player_symbol == gl.AI_O: # If the player is 'O', the AI is 'X' and should start
            self.update_status("AI's turn") # Update status label
            # Schedule the AI's first move after a short delay
            self.window.after(500, self.perform_ai_move)
        else: # If the player is 'X', they start
            self.update_status("Your turn!") # Update status label

    def quit_game(self): # Method called when the Exit button is clicked
        if self.sound_enabled: # If the sound system was initialized
            pygame.mixer.quit() # Properly shut down the pygame mixer module
        self.window.destroy() # Close the main tkinter application window, ending the program

