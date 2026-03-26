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

    # Mergeability bonus: reward adjacent equal tiles (ready to merge)
    merges = 0
    for row in board:
        for i in range(len(row) - 1):
            if row[i] == row[i + 1] and row[i] > 0:
                merges += 1
    for c in range(4):
        col = [board[r][c] for r in range(4)]
        for i in range(len(col) - 1):
            if col[i] == col[i + 1] and col[i] > 0:
                merges += 1

    return emptiness + mono + merges * 50


def choose_move(board, score):
    """2-ply lookahead: evaluate move consequences 2 steps ahead."""
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
        value += evaluate_board(new_board) * 0.3

        # 2-ply lookahead: for each next move, check best third move
        next_valid = get_valid_moves(new_board)
        if next_valid:
            best_continuation = -float('inf')

            for next_dir in next_valid:
                next_board, next_score, _ = move(new_board, next_dir)

                # Value of next move + board quality
                cont_value = next_score + evaluate_board(next_board) * 0.3

                # Best greedy move from the next board (3rd ply)
                next_next_valid = get_valid_moves(next_board)
                if next_next_valid:
                    best_third = 0
                    for third_dir in next_next_valid:
                        third_board, third_score, _ = move(next_board, third_dir)
                        best_third = max(best_third, third_score + evaluate_board(third_board) * 0.3)
                    cont_value += best_third * 0.5

                best_continuation = max(best_continuation, cont_value)

            value += best_continuation * 0.7

        if value > best_value:
            best_value = value
            best_move = direction

    return best_move if best_move else valid[0]
