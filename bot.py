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
    # Monotonicity: reward rows/columns that are monotonic (all increasing or all decreasing)
    mono = 0
    for row in board:
        # Check if row is monotonic (ignoring zeros)
        non_zero = [x for x in row if x > 0]
        if len(non_zero) > 1:
            increasing = all(non_zero[i] <= non_zero[i + 1] for i in range(len(non_zero) - 1))
            decreasing = all(non_zero[i] >= non_zero[i + 1] for i in range(len(non_zero) - 1))
            if increasing or decreasing:
                mono += 5

    for c in range(4):
        col = [board[r][c] for r in range(4)]
        non_zero = [x for x in col if x > 0]
        if len(non_zero) > 1:
            increasing = all(non_zero[i] <= non_zero[i + 1] for i in range(len(non_zero) - 1))
            decreasing = all(non_zero[i] >= non_zero[i + 1] for i in range(len(non_zero) - 1))
            if increasing or decreasing:
                mono += 5

    # Emptiness bonus
    emptiness = count_empty(board) * 100

    return emptiness + mono


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
        value += evaluate_board(new_board) * 0.1

        # 2-ply lookahead: for each next move, check best third move
        next_valid = get_valid_moves(new_board)
        if next_valid:
            best_continuation = -float('inf')

            for next_dir in next_valid:
                next_board, next_score, _ = move(new_board, next_dir)

                # Value of next move + board quality
                cont_value = next_score + evaluate_board(next_board) * 0.1

                # Best greedy move from the next board (3rd ply)
                next_next_valid = get_valid_moves(next_board)
                if next_next_valid:
                    best_third = 0
                    for third_dir in next_next_valid:
                        _, third_score, _ = move(next_board, third_dir)
                        best_third = max(best_third, third_score)
                    cont_value += best_third * 0.3

                best_continuation = max(best_continuation, cont_value)

            value += best_continuation * 0.5

        if value > best_value:
            best_value = value
            best_move = direction

    return best_move if best_move else valid[0]
