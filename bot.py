"""
2048 Bot Strategy — THIS IS THE FILE YOU MODIFY.

The choose_move function is called by the game engine on every turn.
It receives the current board state and score, and must return one of:
'up', 'down', 'left', 'right'
"""

from game import get_valid_moves, move, copy_board


def count_empty(board):
    """Count number of empty cells."""
    return sum(1 for row in board for cell in row if cell == 0)


def evaluate_board(board):
    """Evaluate board position quality (not score, but structural quality)."""
    # Monotonicity: penalty for adjacent tiles in different orders
    mono = 0
    for row in board:
        for i in range(len(row) - 1):
            if (row[i] > row[i + 1]) != (row[0] > row[1]):
                mono -= 1
    for c in range(4):
        col = [board[r][c] for r in range(4)]
        for i in range(len(col) - 1):
            if (col[i] > col[i + 1]) != (col[0] > col[1]):
                mono -= 1

    # Emptiness bonus
    emptiness = count_empty(board) * 50

    return emptiness + mono


def choose_move(board, score):
    """Improved greedy: immediate score + board quality + lookahead."""
    valid = get_valid_moves(board)
    if not valid:
        return 'up'

    best_move = None
    best_value = -float('inf')

    for direction in valid:
        new_board, score_gained, _ = move(board, direction)

        # Immediate reward
        value = score_gained

        # Board quality
        value += evaluate_board(new_board) * 0.1

        # Simple lookahead: try greedy next move
        next_valid = get_valid_moves(new_board)
        if next_valid:
            lookahead_scores = []
            for next_dir in next_valid:
                _, next_score, _ = move(new_board, next_dir)
                lookahead_scores.append(next_score)
            if lookahead_scores:
                value += max(lookahead_scores) * 0.5

        if value > best_value:
            best_value = value
            best_move = direction

    return best_move if best_move else valid[0]
