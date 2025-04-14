import math
import random

PLAYER_X = 'X'
AI_O = 'O'
EMPTY = ' '

EASY = "Easy"
MEDIUM = "Medium"
HARD = "Hard"

def init_board():
    """Create and return an empty 3x3 game board."""
    return [[EMPTY for _ in range(3)] for _ in range(3)]

def get_available_moves(board):
    """Return list of (row, col) tuples for empty cells."""
    return [(i, j) for i in range(3) for j in range(3) if board[i][j] == EMPTY]

def is_board_full(board):
    """Check if board has no empty cells left."""
    return all(board[i][j] != EMPTY for i in range(3) for j in range(3))

def check_winner(board, player):
    """Check if specified player has won."""
    for i in range(3):
        if all(board[i][j] == player for j in range(3)): return True
        if all(board[j][i] == player for j in range(3)): return True
    if all(board[i][i] == player for i in range(3)): return True
    if all(board[i][2 - i] == player for i in range(3)): return True
    return False

def get_winning_line(board):
    """Return winning line coordinates if there's a winner."""
    for r in range(3):
        if all(board[r][c] == board[r][0] and board[r][0] != EMPTY for c in range(3)):
            return [(r, c) for c in range(3)]
    for c in range(3):
        if all(board[r][c] == board[0][c] and board[0][c] != EMPTY for r in range(3)):
            return [(r, c) for r in range(3)]
    if all(board[i][i] == board[0][0] and board[0][0] != EMPTY for i in range(3)):
        return [(i, i) for i in range(3)]
    if all(board[i][2 - i] == board[0][2] and board[0][2] != EMPTY for i in range(3)):
        return [(i, 2 - i) for i in range(3)]
    return None

def evaluate_board(board, ai_symbol, player_symbol):
    """Evaluate board state for the AI."""
    if check_winner(board, ai_symbol): return 1
    elif check_winner(board, player_symbol): return -1
    else: return 0

def minimax(board, depth, is_maximizing, alpha, beta, ai_symbol, player_symbol):
    """Minimax algorithm with alpha-beta pruning."""
    score = evaluate_board(board, ai_symbol, player_symbol)

    if score == 1 or score == -1: return score
    if is_board_full(board): return 0

    available_moves = get_available_moves(board)

    if is_maximizing:
        best_score = -math.inf
        for move in available_moves:
            board[move[0]][move[1]] = ai_symbol
            current_score = minimax(board, depth + 1, False, alpha, beta, ai_symbol, player_symbol)
            board[move[0]][move[1]] = EMPTY
            best_score = max(best_score, current_score)
            alpha = max(alpha, best_score)
            if beta <= alpha:
                break
        return best_score
    else:
        best_score = math.inf
        for move in available_moves:
            board[move[0]][move[1]] = player_symbol
            current_score = minimax(board, depth + 1, True, alpha, beta, ai_symbol, player_symbol)
            board[move[0]][move[1]] = EMPTY
            best_score = min(best_score, current_score)
            beta = min(beta, best_score)
            if beta <= alpha:
                break
        return best_score

def ai_move(board, difficulty=HARD, ai_symbol=AI_O):
    """Determine AI move based on difficulty level."""
    available_moves = get_available_moves(board)
    if not available_moves: return None

    player_symbol = PLAYER_X if ai_symbol == AI_O else AI_O

    if difficulty == EASY:
        return random.choice(available_moves)

    elif difficulty == MEDIUM:
        for move in available_moves:
            board[move[0]][move[1]] = ai_symbol
            if check_winner(board, ai_symbol):
                board[move[0]][move[1]] = EMPTY
                return move
            board[move[0]][move[1]] = EMPTY

        for move in available_moves:
            board[move[0]][move[1]] = player_symbol
            if check_winner(board, player_symbol):
                board[move[0]][move[1]] = EMPTY
                return move
            board[move[0]][move[1]] = EMPTY

        return (_find_best_move_minimax(board, ai_symbol, player_symbol)
                if random.random() < 0.5 else random.choice(available_moves))

    elif difficulty == HARD:
        if len(available_moves) == 9:
            return random.choice([(0,0), (0,2), (2,0), (2,2), (1,1)])
        if len(available_moves) == 8 and board[1][1] == EMPTY:
            return (1,1)
        return _find_best_move_minimax(board, ai_symbol, player_symbol)

    else:
        print(f"Warning: Unknown difficulty '{difficulty}'. Defaulting to Hard.")
        return _find_best_move_minimax(board, ai_symbol, player_symbol)

def _find_best_move_minimax(board, ai_symbol, player_symbol):
    """Helper function to find best move using minimax."""
    best_score = -math.inf
    best_move = None
    available_moves = get_available_moves(board)
    random.shuffle(available_moves)

    for move in available_moves:
        board[move[0]][move[1]] = ai_symbol
        score = minimax(board, 0, False, -math.inf, math.inf, ai_symbol, player_symbol)
        board[move[0]][move[1]] = EMPTY

        if score > best_score:
            best_score = score
            best_move = move

    return best_move if best_move is not None else available_moves[0]
