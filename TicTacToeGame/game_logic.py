import math # Import the math module for functions like infinity (math.inf)
import random # Import the random module for making random choices (used in AI)

# Constants
PLAYER_X = 'X' # Define a constant for the player's symbol (X)
AI_O = 'O' # Define a constant for the AI's symbol (O)
EMPTY = ' ' # Define a constant for an empty cell on the board

# Difficulty Levels
EASY = "Easy" # Define a constant string for the Easy difficulty level
MEDIUM = "Medium" # Define a constant string for the Medium difficulty level
HARD = "Hard" # Define a constant string for the Hard difficulty level

def init_board(): # Defines a function to initialize the game board
    """Create and return an empty 3x3 game board."""
    # Use nested list comprehensions to create a 3x3 list filled with the EMPTY constant
    return [[EMPTY for _ in range(3)] for _ in range(3)]

def get_available_moves(board): # Defines a function to find all empty cells on the board
    """Return list of (row, col) tuples for empty cells."""
    # Use a list comprehension to iterate through all cells (i=row, j=column)
    # If a cell board[i][j] is EMPTY, add its coordinates (i, j) as a tuple to the list
    return [(i, j) for i in range(3) for j in range(3) if board[i][j] == EMPTY]

def is_board_full(board): # Defines a function to check if the board has any empty cells left
    """Check if board has no empty cells left."""
    # Use the 'all()' function with a generator expression
    # It checks if *all* cells (board[i][j]) in the 3x3 grid are *not* equal to EMPTY
    # Returns True if the board is full, False otherwise
    return all(board[i][j] != EMPTY for i in range(3) for j in range(3))

def check_winner(board, player): # Defines a function to check if a specific player ('X' or 'O') has won
    """Check if specified player has won."""
    # Check rows and columns
    for i in range(3): # Loop through rows/columns index (0, 1, 2)
        # Check if all cells in the current row 'i' contain the player's symbol
        if all(board[i][j] == player for j in range(3)): return True
        # Check if all cells in the current column 'i' contain the player's symbol
        if all(board[j][i] == player for j in range(3)): return True
    # Check diagonals
    # Check the main diagonal (top-left to bottom-right)
    if all(board[i][i] == player for i in range(3)): return True
    # Check the anti-diagonal (top-right to bottom-left)
    if all(board[i][2 - i] == player for i in range(3)): return True
    # If none of the above conditions are met, the player has not won
    return False

def get_winning_line(board): # Defines a function to find the coordinates of the winning line, if one exists
    """Return winning line coordinates if there's a winner."""
    # Check rows
    for r in range(3): # Loop through each row index (0, 1, 2)
        # Check if all cells in row 'r' are the same and not EMPTY
        if all(board[r][c] == board[r][0] and board[r][0] != EMPTY for c in range(3)):
            # If a winning row is found, return a list of (row, col) tuples for that row
            return [(r, c) for c in range(3)]
    # Check columns
    for c in range(3): # Loop through each column index (0, 1, 2)
        # Check if all cells in column 'c' are the same and not EMPTY
        if all(board[r][c] == board[0][c] and board[0][c] != EMPTY for r in range(3)):
            # If a winning column is found, return a list of (row, col) tuples for that column
            return [(r, c) for r in range(3)]
    # Check diagonals
    # Check main diagonal (top-left to bottom-right)
    if all(board[i][i] == board[0][0] and board[0][0] != EMPTY for i in range(3)):
        # If the main diagonal is winning, return its coordinates
        return [(i, i) for i in range(3)]
    # Check anti-diagonal (top-right to bottom-left)
    if all(board[i][2 - i] == board[0][2] and board[0][2] != EMPTY for i in range(3)):
        # If the anti-diagonal is winning, return its coordinates
        return [(i, 2 - i) for i in range(3)]
    # If no winning line is found, return None
    return None

def evaluate_board(board, ai_symbol, player_symbol): # Defines a function to evaluate the board state from the AI's perspective
    """Evaluate board state for the AI."""
    # Check if the AI has won
    if check_winner(board, ai_symbol): return 1 # Return 1 (positive score) if AI wins
    # Check if the Player has won
    elif check_winner(board, player_symbol): return -1 # Return -1 (negative score) if Player wins
    # If neither has won (could be ongoing or a draw)
    else: return 0 # Return 0 for a draw or ongoing game

def minimax(board, depth, is_maximizing, alpha, beta, ai_symbol, player_symbol): # Defines the minimax algorithm with alpha-beta pruning
    """Minimax algorithm with alpha-beta pruning."""
    # Evaluate the current board state
    score = evaluate_board(board, ai_symbol, player_symbol)

    # Base cases for recursion:
    # If the AI won (score=1) or the Player won (score=-1), return the score
    if score == 1 or score == -1: return score
    # If the board is full (draw), return 0
    if is_board_full(board): return 0

    # Get list of possible moves
    available_moves = get_available_moves(board)

    if is_maximizing: # If it's the AI's turn (Maximizing player)
        best_score = -math.inf # Initialize best score to negative infinity
        # Iterate through each available move
        for move in available_moves:
            board[move[0]][move[1]] = ai_symbol # Temporarily make the AI move
            # Recursively call minimax for the opponent's turn (minimizing player)
            current_score = minimax(board, depth + 1, False, alpha, beta, ai_symbol, player_symbol)
            board[move[0]][move[1]] = EMPTY # Undo the move
            best_score = max(best_score, current_score) # Update best score found so far
            alpha = max(alpha, best_score) # Update alpha (best score for maximizer along this path)
            if beta <= alpha: # Alpha-beta pruning condition: if beta <= alpha, prune this branch
                break # Stop exploring further moves in this branch
        return best_score # Return the best score found for the maximizing player
    else: # If it's the Player's turn (Minimizing player)
        best_score = math.inf # Initialize best score to positive infinity
        # Iterate through each available move
        for move in available_moves:
            board[move[0]][move[1]] = player_symbol # Temporarily make the Player move
            # Recursively call minimax for the AI's turn (maximizing player)
            current_score = minimax(board, depth + 1, True, alpha, beta, ai_symbol, player_symbol)
            board[move[0]][move[1]] = EMPTY # Undo the move
            best_score = min(best_score, current_score) # Update best score found so far (want the minimum for opponent)
            beta = min(beta, best_score) # Update beta (best score for minimizer along this path)
            if beta <= alpha: # Alpha-beta pruning condition
                break # Stop exploring further moves in this branch
        return best_score # Return the best score found for the minimizing player

def ai_move(board, difficulty=HARD, ai_symbol=AI_O): # Defines the main function to determine the AI's next move based on difficulty
    """Determine AI move based on difficulty level."""
    # Get all currently available moves
    available_moves = get_available_moves(board)
    # If there are no moves left, return None (shouldn't happen if called correctly)
    if not available_moves: return None

    # Determine the player's symbol based on the AI's symbol
    player_symbol = PLAYER_X if ai_symbol == AI_O else AI_O

    # --- Difficulty Logic ---
    if difficulty == EASY: # If difficulty is Easy
        # Simply return a random move from the available options
        return random.choice(available_moves)

    elif difficulty == MEDIUM: # If difficulty is Medium
        # 1. Check for immediate win: Iterate through moves, if placing AI symbol results in a win, take that move.
        for move in available_moves:
            board[move[0]][move[1]] = ai_symbol # Try placing AI symbol
            if check_winner(board, ai_symbol): # Check if this wins
                board[move[0]][move[1]] = EMPTY # Undo move before returning
                return move # Return the winning move
            board[move[0]][move[1]] = EMPTY # Undo move if it wasn't a win

        # 2. Check for immediate block: Iterate through moves, if placing Player symbol results in a Player win, block that move.
        for move in available_moves:
            board[move[0]][move[1]] = player_symbol # Try placing Player symbol (to check if they would win there)
            if check_winner(board, player_symbol): # Check if player wins at this spot
                board[move[0]][move[1]] = EMPTY # Undo move before returning
                return move # Return the blocking move
            board[move[0]][move[1]] = EMPTY # Undo move if it wasn't a player win

        # 3. 50/50 chance: Either use Minimax (Hard logic) or make a random move
        return (_find_best_move_minimax(board, ai_symbol, player_symbol) # Call minimax helper
                if random.random() < 0.5 else random.choice(available_moves)) # Or choose randomly

    elif difficulty == HARD: # If difficulty is Hard
        # Opening move optimization: If board is empty, choose a random corner or center
        if len(available_moves) == 9:
            return random.choice([(0,0), (0,2), (2,0), (2,2), (1,1)])
        # Second move optimization: If center is free after first move, take it
        if len(available_moves) == 8 and board[1][1] == EMPTY:
            return (1,1)
        # Otherwise, use the Minimax algorithm to find the optimal move
        return _find_best_move_minimax(board, ai_symbol, player_symbol)

    else: # If an unknown difficulty string is passed
        # Print a warning message
        print(f"Warning: Unknown difficulty '{difficulty}'. Defaulting to Hard.")
        # Default to using the Minimax algorithm (Hard difficulty behavior)
        return _find_best_move_minimax(board, ai_symbol, player_symbol)

def _find_best_move_minimax(board, ai_symbol, player_symbol): # Defines a helper function specifically for finding the best move using minimax
    """Helper function to find best move using minimax."""
    best_score = -math.inf # Initialize the best score found so far to negative infinity
    best_move = None # Initialize the best move found so far to None
    available_moves = get_available_moves(board) # Get the list of available moves
    random.shuffle(available_moves) # Shuffle moves to add randomness among equally good moves

    # Iterate through all available moves
    for move in available_moves:
        board[move[0]][move[1]] = ai_symbol # Temporarily make the AI move
        # Call the minimax function to evaluate this move. Start depth 0, opponent's turn (is_maximizing=False).
        # Pass initial alpha (-inf) and beta (+inf).
        score = minimax(board, 0, False, -math.inf, math.inf, ai_symbol, player_symbol)
        board[move[0]][move[1]] = EMPTY # Undo the move

        # If the score for this move is better than the best score found so far
        if score > best_score:
            best_score = score # Update the best score
            best_move = move # Update the best move

    # Return the best move found. If no move improved the score (e.g., all lead to loss), return the first shuffled available move as a fallback.
    return best_move if best_move is not None else available_moves[0]