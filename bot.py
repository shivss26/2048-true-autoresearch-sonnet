"""
2048 Bot Strategy — THIS IS THE FILE YOU MODIFY.

The choose_move function is called by the game engine on every turn.
It receives the current board state and score, and must return one of:
'up', 'down', 'left', 'right'
"""

from game import get_valid_moves, move, copy_board


def choose_move(board, score):
    """Greedy strategy: pick the move that maximizes immediate score gain."""
    valid = get_valid_moves(board)
    if not valid:
        return 'up'

    best_move = None
    best_score = -1

    for direction in valid:
        _, score_gained, _ = move(board, direction)
        if score_gained > best_score:
            best_score = score_gained
            best_move = direction

    return best_move if best_move else valid[0]
