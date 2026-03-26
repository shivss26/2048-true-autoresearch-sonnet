"""
2048 Game Engine — DO NOT MODIFY.

This is the fixed evaluation harness, equivalent to prepare.py in
Karpathy's autoresearch. The bot strategy in bot.py is the only
thing that should change during experiments.
"""

import random
import copy

SIZE = 4


def new_game(seed=None):
    """Create a new 2048 game state. Returns (board, score, rng)."""
    rng = random.Random(seed)
    board = [[0] * SIZE for _ in range(SIZE)]
    _spawn_tile(board, rng)
    _spawn_tile(board, rng)
    return board, 0, rng


def _spawn_tile(board, rng):
    """Place a 2 (90%) or 4 (10%) on a random empty cell."""
    empty = [(r, c) for r in range(SIZE) for c in range(SIZE) if board[r][c] == 0]
    if not empty:
        return
    r, c = rng.choice(empty)
    board[r][c] = 2 if rng.random() < 0.9 else 4


def _slide_row_left(row):
    """Slide and merge a single row to the left. Returns (new_row, score_gained)."""
    # Remove zeros
    tiles = [x for x in row if x != 0]
    merged = []
    score = 0
    skip = False
    for i in range(len(tiles)):
        if skip:
            skip = False
            continue
        if i + 1 < len(tiles) and tiles[i] == tiles[i + 1]:
            val = tiles[i] * 2
            merged.append(val)
            score += val
            skip = True
        else:
            merged.append(tiles[i])
    # Pad with zeros
    merged.extend([0] * (SIZE - len(merged)))
    return merged, score


def move(board, direction):
    """
    Execute a move. direction is one of: 'left', 'right', 'up', 'down'.
    Returns (new_board, score_gained, changed).
    changed is False if the move had no effect (invalid move).
    """
    # Rotate board so we always slide left, then rotate back
    rotated = _rotate_for_direction(board, direction)

    new_board = []
    total_score = 0
    for row in rotated:
        new_row, score = _slide_row_left(row)
        new_board.append(new_row)
        total_score += score

    new_board = _rotate_back(new_board, direction)

    changed = new_board != board
    return new_board, total_score, changed


def _rotate_for_direction(board, direction):
    """Rotate board so that the desired direction becomes 'left'."""
    if direction == 'left':
        return [row[:] for row in board]
    elif direction == 'right':
        return [row[::-1] for row in board]
    elif direction == 'up':
        # Transpose
        return [[board[r][c] for r in range(SIZE)] for c in range(SIZE)]
    elif direction == 'down':
        # Transpose then reverse each row
        return [[board[r][c] for r in range(SIZE)][::-1] for c in range(SIZE)]
    raise ValueError(f"Invalid direction: {direction}")


def _rotate_back(board, direction):
    """Undo the rotation applied by _rotate_for_direction."""
    if direction == 'left':
        return board
    elif direction == 'right':
        return [row[::-1] for row in board]
    elif direction == 'up':
        return [[board[c][r] for c in range(SIZE)] for r in range(SIZE)]
    elif direction == 'down':
        return [[board[c][SIZE - 1 - r] for c in range(SIZE)] for r in range(SIZE)]
    raise ValueError(f"Invalid direction: {direction}")


def move_and_spawn(board, direction, rng):
    """Execute a move and spawn a new tile if the move was valid.
    Returns (new_board, score_gained, valid)."""
    new_board, score, changed = move(board, direction)
    if changed:
        _spawn_tile(new_board, rng)
    return new_board, score, changed


DIRECTIONS = ['up', 'down', 'left', 'right']


def get_valid_moves(board):
    """Return list of directions that would change the board."""
    valid = []
    for d in DIRECTIONS:
        _, _, changed = move(board, d)
        if changed:
            valid.append(d)
    return valid


def is_game_over(board):
    """True if no valid moves remain."""
    return len(get_valid_moves(board)) == 0


def get_max_tile(board):
    """Return the highest tile value on the board."""
    return max(max(row) for row in board)


def copy_board(board):
    """Deep copy a board."""
    return [row[:] for row in board]


def print_board(board):
    """Pretty-print the board."""
    width = max(len(str(cell)) for row in board for cell in row)
    separator = '+' + ('+'.join(['-' * (width + 2)] * SIZE)) + '+'
    print(separator)
    for row in board:
        cells = '|'.join(str(cell).center(width + 2) if cell != 0 else ' ' * (width + 2) for cell in row)
        print('|' + cells + '|')
        print(separator)


def play_game(bot_fn, seed=None):
    """
    Play a complete game using bot_fn to choose moves.

    bot_fn(board, score) -> direction string ('up','down','left','right')

    Returns (final_score, max_tile, num_moves).
    """
    board, score, rng = new_game(seed)
    num_moves = 0

    while not is_game_over(board):
        direction = bot_fn(board, score)

        if direction not in DIRECTIONS:
            # Invalid direction from bot, skip
            break

        new_board, gained, valid = move_and_spawn(board, direction, rng)
        if not valid:
            # Bot chose a move that doesn't change the board.
            # Give it one more chance with valid moves.
            valid_moves = get_valid_moves(board)
            if not valid_moves:
                break
            # Just pick the first valid move as fallback
            direction = valid_moves[0]
            new_board, gained, valid = move_and_spawn(board, direction, rng)

        board = new_board
        score += gained
        num_moves += 1

    return score, get_max_tile(board), num_moves
