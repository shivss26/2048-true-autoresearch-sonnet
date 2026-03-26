"""
2048 Bot Evaluator — DO NOT MODIFY.

Runs the bot from bot.py over 50 fixed-seed games and reports metrics.
This is the measurement harness. Only bot.py should change.

Usage: python evaluate.py
"""

import time
import sys

from game import play_game
from bot import choose_move

NUM_GAMES = 50
TIME_LIMIT = 60  # seconds


def evaluate():
    scores = []
    max_tiles = []
    start = time.time()

    for seed in range(NUM_GAMES):
        score, max_tile, num_moves = play_game(choose_move, seed=seed)
        scores.append(score)
        max_tiles.append(max_tile)

        elapsed = time.time() - start
        if elapsed > TIME_LIMIT:
            print(f"TIME LIMIT EXCEEDED after {seed + 1} games ({elapsed:.1f}s)")
            sys.exit(1)

    elapsed = time.time() - start

    avg_score = sum(scores) / len(scores)
    best_score = max(scores)
    worst_score = min(scores)
    max_tile = max(max_tiles)
    pct_512 = sum(1 for t in max_tiles if t >= 512) / len(max_tiles) * 100
    pct_1024 = sum(1 for t in max_tiles if t >= 1024) / len(max_tiles) * 100
    pct_2048 = sum(1 for t in max_tiles if t >= 2048) / len(max_tiles) * 100

    print("===== 2048 BOT EVALUATION =====")
    print(f"avg_score:    {avg_score:.1f}")
    print(f"best_score:   {best_score}")
    print(f"worst_score:  {worst_score}")
    print(f"max_tile:     {max_tile}")
    print(f"pct_512:      {pct_512:.0f}%")
    print(f"pct_1024:     {pct_1024:.0f}%")
    print(f"pct_2048:     {pct_2048:.0f}%")
    print(f"time_sec:     {elapsed:.1f}")
    print(f"games:        {NUM_GAMES}")
    print("===============================")


if __name__ == "__main__":
    evaluate()
