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
    # Monotonicity: strongly penalize disorder in rows/cols
    mono = 0

    # Check each row for monotonicity
    for row in board:
        for i in range(len(row) - 1):
            # If non-zero tiles are out of order, penalize
            if row[i] != 0 and row[i + 1] != 0:
                if row[i] > row[i + 1]:
                    mono -= 2  # Decreasing
                # Increasing is okay

    # Check each column for monotonicity
    for c in range(4):
        col = [board[r][c] for r in range(4)]
        for i in range(len(col) - 1):
            if col[i] != 0 and col[i + 1] != 0:
                if col[i] > col[i + 1]:
                    mono -= 2

    # Emptiness bonus: more empty cells = more room to merge
    emptiness = count_empty(board) * 100

    # Cluster bonus: reward tiles that are close together (helps merging)
    cluster = 0
    for r in range(4):
        for c in range(4):
            if board[r][c] > 0:
                # Check neighbors: adjacent same-value tiles are good
                neighbors = 0
                if c > 0 and board[r][c - 1] == board[r][c]:
                    neighbors += 1
                if c < 3 and board[r][c + 1] == board[r][c]:
                    neighbors += 1
                if r > 0 and board[r - 1][c] == board[r][c]:
                    neighbors += 1
                if r < 3 and board[r + 1][c] == board[r][c]:
                    neighbors += 1
                cluster += neighbors * board[r][c] * 2

    # Corner bonus: reward keeping large tiles in corners
    corner_bonus = 0
    corners = [(0, 0), (0, 3), (3, 0), (3, 3)]
    for r, c in corners:
        if board[r][c] > 256:
            corner_bonus += board[r][c] * 2

    return emptiness + mono + cluster + corner_bonus


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
