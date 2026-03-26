"""
2048 Bot Strategy — THIS IS THE FILE YOU MODIFY.

The choose_move function is called by the game engine on every turn.
It receives the current board state and score, and must return one of:
'up', 'down', 'left', 'right'
"""

from game import get_valid_moves


def choose_move(board, score):
    """Pick a move given the current board and score.

    Baseline strategy: pick the first valid move in a fixed order.
    This is the dumbest possible strategy — it doesn't even look
    at the board state, just tries moves in order.
    """
    valid = get_valid_moves(board)
    if not valid:
        return 'up'

    # Just pick the first valid move. No strategy at all.
    for direction in ['up', 'left', 'down', 'right']:
        if direction in valid:
            return direction

    return valid[0]
