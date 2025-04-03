# themes.py
"""
Contains theme definitions for the Tic-Tac-Toe GUI.
Each theme is a dictionary mapping element types to color codes.
Added optional keys for the title bar and window controls.
"""

THEMES = {
    "Sci-Fi": {
        "bg": "#0d1b2a",        # Dark blue background
        "btn_bg": "#1b263b",    # Button default background
        "hover": "#415a77",     # Button hover background
        "clicked": "#778da9",   # Button clicked/occupied background
        "text": "#E0E1DD",      # Default text color (e.g., status)
        "player": "#00f5d4",    # Player 'X' color (bright cyan)
        "ai": "#ff006e",        # AI 'O' color (bright pink)
        "win": "#ffd700",       # Winning line highlight (gold)
        "score": "#E0E1DD",     # Scoreboard text color
        "control_bg": "#00b359", # Restart button background
        "control_fg": "#FFFFFF", # Restart button text
        "control_active": "#00994d", # Restart button active background
        "exit_bg": "#e63946",   # Exit button background (reddish)
        "exit_fg": "#FFFFFF",   # Exit button text
        "exit_active": "#d00000", # Exit button active background
        "title_bg": "#1b263b",  # Title bar background
        "title_fg": "#E0E1DD",  # Title text color
        "title_btn_bg": "#3a3a3a", # Title button background
        "title_btn_fg": "#ffffff"  # Title button text color
    },
    "Retro": {
        "bg": "#2b2d42",        # Dark gray-blue background
        "btn_bg": "#8d99ae",    # Gray button default background
        "hover": "#adb5bd",     # Light gray hover
        "clicked": "#ced4da",   # Very light gray clicked/occupied background
        "text": "#edf2f4",      # Off-white text color
        "player": "#ef233c",    # Bright Red player 'X'
        "ai": "#ffd166",        # Yellow AI 'O'
        "win": "#06d6a0",       # Green winning line highlight
        "score": "#edf2f4",     # Scoreboard text color
        "control_bg": "#d90429", # Restart button background (red)
        "control_fg": "#FFFFFF", # Restart button text
        "control_active": "#b30321", # Restart button active background
        "exit_bg": "#fb8500",   # Exit button background (orange)
        "exit_fg": "#023047",   # Exit button text (dark blue)
        "exit_active": "#e85d04", # Exit button active background
        "title_bg": "#2b2d42",  # Title bar background
        "title_fg": "#edf2f4",  # Title text color
        "title_btn_bg": "#3a3a3a", # Title button background
        "title_btn_fg": "#ffffff"  # Title button text color
    },
    "Forest": {
        "bg": "#2d6a4f",        # Dark green background
        "btn_bg": "#40916c",    # Medium green button background
        "hover": "#52b788",     # Lighter green hover
        "clicked": "#74c69d",   # Even lighter green clicked/occupied
        "text": "#d8f3dc",      # Pale green text
        "player": "#ffffff",    # White player 'X'
        "ai": "#ffba08",        # Orange AI 'O'
        "win": "#ffccd5",       # Pink winning highlight
        "score": "#d8f3dc",     # Scoreboard text color
        "control_bg": "#95d5b2", # Restart button background (light green)
        "control_fg": "#081c15", # Restart button text (dark green)
        "control_active": "#74c69d", # Restart button active background
        "exit_bg": "#bc4749",   # Exit button background (brownish red)
        "exit_fg": "#f2e8cf",   # Exit button text (light beige)
        "exit_active": "#a44a3f", # Exit button active background
        "title_bg": "#2d6a4f",  # Title bar background
        "title_fg": "#d8f3dc",  # Title text color
        "title_btn_bg": "#3a3a3a", # Title button background
        "title_btn_fg": "#ffffff"  # Title button text color
    },
    "Dark Mode": {
        "bg": "#121212",        # Very dark gray background
        "btn_bg": "#1e1e1e",   # Slightly lighter gray buttons
        "hover": "#2e2e2e",     # Hover state
        "clicked": "#3e3e3e",   # Clicked state
        "text": "#e0e0e0",      # Light gray text
        "player": "#4fc3f7",    # Light blue player
        "ai": "#ff8a65",        # Light orange AI
        "win": "#ffd54f",       # Yellow winning line
        "score": "#e0e0e0",     # Score text
        "control_bg": "#424242", # Control buttons
        "control_fg": "#ffffff", # Control text
        "control_active": "#616161", # Active control
        "exit_bg": "#d32f2f",   # Red exit button
        "exit_fg": "#ffffff",   # Exit text
        "exit_active": "#b71c1c", # Active exit
        "title_bg": "#1e1e1e",  # Title bar
        "title_fg": "#ffffff",  # Title text
        "title_btn_bg": "#424242", # Title buttons
        "title_btn_fg": "#ffffff"  # Title button text
    },
    "Ocean": {
        "bg": "#006994",        # Deep ocean blue
        "btn_bg": "#0077b6",    # Button color
        "hover": "#0096c7",     # Hover
        "clicked": "#00b4d8",   # Clicked
        "text": "#ffffff",      # White text
        "player": "#ffd166",    # Yellow player
        "ai": "#ef476f",        # Pink AI
        "win": "#06d6a0",       # Green winning line
        "score": "#ffffff",     # Score text
        "control_bg": "#48cae4", # Control buttons
        "control_fg": "#03045e", # Control text
        "control_active": "#90e0ef", # Active control
        "exit_bg": "#ef476f",   # Red exit button
        "exit_fg": "#ffffff",   # Exit text
        "exit_active": "#ff758f", # Active exit
        "title_bg": "#0077b6",  # Title bar
        "title_fg": "#ffffff",  # Title text
        "title_btn_bg": "#0096c7", # Title buttons
        "title_btn_fg": "#ffffff"  # Title button text
    },
    "Sunset": {
        "bg": "#ff9e7d",        # Light orange background
        "btn_bg": "#ffb3a7",    # Button color
        "hover": "#ffcdb2",     # Hover
        "clicked": "#ffddd2",   # Clicked
        "text": "#6d6875",      # Dark gray text
        "player": "#b5838d",    # Muted purple player
        "ai": "#6d6875",        # Dark gray AI
        "win": "#e5989b",       # Pink winning line
        "score": "#6d6875",     # Score text
        "control_bg": "#b5838d", # Control buttons
        "control_fg": "#ffffff", # Control text
        "control_active": "#d8a48f", # Active control
        "exit_bg": "#6d6875",   # Dark gray exit button
        "exit_fg": "#ffffff",   # Exit text
        "exit_active": "#56505a", # Active exit
        "title_bg": "#ffb3a7",  # Title bar
        "title_fg": "#6d6875",  # Title text
        "title_btn_bg": "#b5838d", # Title buttons
        "title_btn_fg": "#ffffff"  # Title button text
    }
}

DEFAULT_THEME = "Sci-Fi"