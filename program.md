# 2048 Bot Autoresearch (Autonomous)

You are an autonomous game AI researcher. Your job is to improve a 2048 bot's average score through iterative strategy experiments.

## Setup

1. **Check if an experiment branch exists.** Run `git branch`. If `autoresearch` branch exists, switch to it. If not, create it: `git checkout -b autoresearch`. All work happens on this branch, never on master.
2. **Read the in-scope files** for full context:
   - `game.py` — the 2048 game engine. DO NOT MODIFY.
   - `evaluate.py` — runs 50 games and reports metrics. DO NOT MODIFY.
   - `bot.py` — the bot strategy. This is the only file you edit.
3. **Read `results.tsv`** to see what experiments have already been tried. Do NOT repeat experiments that were already discarded. Build on what worked.
4. **Run a baseline evaluation** if results.tsv has no entries yet: run `python evaluate.py`, log the result as the `baseline` row, commit, and push.

## Experimentation

Each experiment modifies the bot strategy and measures the result by running `python evaluate.py`.

**What you CAN do:**
- Modify `bot.py`. This is the only file you edit.
- Change anything about the strategy: heuristics, evaluation functions, search depth, move ordering, weights.
- Import from `game.py` (it exposes helper functions like `move`, `get_valid_moves`, `copy_board`, etc.).
- Use Python standard library modules.

**What you CANNOT do:**
- Modify `game.py`. It is read-only.
- Modify `evaluate.py`. It is read-only.
- Modify `program.md`. It is read-only.
- Modify `results.tsv` except to append new rows.
- Install new packages. Only standard library + game.py imports.

**The goal is simple: get the highest average score over 50 fixed-seed games.** Secondary goals: highest max tile reached, highest % of games reaching the 2048 tile. The evaluation uses seeds 0-49, so results are deterministic for the same strategy.

**Time budget**: The 50-game evaluation must complete in under 60 seconds. This prevents brute-force deep search from being the only viable strategy — you need smart heuristics, not just more compute.

**Simplicity criterion**: All else being equal, simpler is better. A small improvement that adds ugly complexity is not worth it. Clean, readable strategy code that scores well is the goal.

## Measurement

Run the evaluation exactly ONCE per experiment:
```
python evaluate.py
```

This outputs:
```
===== 2048 BOT EVALUATION =====
avg_score:    2340.2
best_score:   5832
worst_score:  684
max_tile:     512
pct_512:      24%
pct_1024:     4%
pct_2048:     0%
time_sec:     1.3
games:        50
===============================
```

The key metric is `avg_score`. Do NOT run the evaluation more than once per experiment. Do NOT guess or estimate scores.

## Output format

After each evaluation, report scores like this:

```
===== 2048 EXPERIMENT RESULTS =====
avg_score (before):   XXXX.X
avg_score (after):    XXXX.X
change:               +/-XXX.X
status:               keep/discard
====================================
```

## Logging results

Log every experiment to `results.tsv` (tab-separated, NOT comma-separated).

The TSV has a header row and 8 columns:

```
commit	avg_score	best_score	max_tile	pct_2048	time_sec	status	description
```

1. git commit hash (short, 7 chars)
2. avg_score over 50 games
3. best single-game score
4. highest tile reached across all games
5. percentage of games reaching 2048 tile
6. evaluation time in seconds
7. status: `baseline`, `keep`, or `discard`
8. short text description of what this experiment tried

Example:

```
commit	avg_score	best_score	max_tile	pct_2048	time_sec	status	description
a1b2c3d	2340.2	5832	512	0	1.3	baseline	fixed move order, no strategy
b2c3d4e	4210.5	12044	1024	0	1.8	keep	greedy - pick highest immediate score
c3d4e5f	3890.1	9216	1024	0	2.1	discard	always prefer down then right
```

## The experiment loop

All work happens on the `autoresearch` branch. Every experiment is committed and pushed so the full history is visible.

LOOP:

1. Read the current `bot.py` and `results.tsv` to understand the current state and what's been tried.
2. Propose a hypothesis: decide what to change and why you think it will improve scores.
3. Make the change to `bot.py`.
4. `git add bot.py`, `git commit` with a descriptive message prefixed with `[EXPERIMENT]`.
5. Update `results.tsv` with a new row (status TBD, leave as `pending` for now). Amend the commit: `git add results.tsv && git commit --amend --no-edit`.
6. Run `python evaluate.py` exactly once. Record the scores.
7. Compare avg_score against the previous baseline (the most recent `keep` or `baseline` row in results.tsv).
8. Decide: keep or discard? Use these rules strictly:
   - **KEEP** if `avg_score` strictly improved (even by 0.1). `avg_score` is the only decision metric. Other metrics (best_score, max_tile, pct_2048) are useful context for planning future experiments but do NOT affect the keep/discard decision.
   - **DISCARD** if `avg_score` stayed the same or decreased — even if other metrics improved. Note any promising secondary metrics in the description so the next agent can refine the approach.
   - **DISCARD** if evaluation exceeded the 60-second time limit (DNF). Log `DNF` for avg_score.
   - If kept: Update the `pending` row in results.tsv to `keep`. Commit with message `[KEEP] <description>` and push.
   - If discarded: Revert `bot.py` back to the previous baseline state. Update the `pending` row to `discard`. Commit with message `[DISCARD] revert: <description>` and push.
9. **STOP. You are done. Exit immediately after this step.** Do not start another experiment. Do not loop back to step 1. The wrapper script will spawn a fresh agent for the next experiment.

**Commit message format:**
- Experiment + TSV log: `[EXPERIMENT] added corner heuristic to evaluation`
- Kept (after measurement): `[KEEP] added corner heuristic to evaluation`
- Discarded (revert + log): `[DISCARD] revert: added corner heuristic to evaluation`

This means each experiment produces exactly 2 commits: the experiment itself, and the keep/discard result.

**Target: avg_score 30,000+.** Once you hit this on a kept experiment, log it, then create a file called `TARGET_REACHED` containing the final avg_score, and exit.

**If `TARGET_REACHED` already exists when you start**, the target has been met in a previous session. Do nothing and exit immediately.

## Important rules

- **One change at a time.** Each experiment should test ONE idea. Don't bundle multiple heuristics.
- **Don't repeat failed experiments.** Always read results.tsv first. If something was already tried and discarded, don't try it again.
- **The baseline ratchets forward.** When an experiment is kept, it becomes the new baseline. Always compare against the most recent kept version.
- **Run evaluation exactly once per experiment.** Do not retry. If it fails, log the experiment as `error` and exit.
- **Never work on master.** All experiments happen on the `autoresearch` branch.
- **CRITICAL: Do exactly ONE experiment per session, then exit.** You must exit after step 9. Do NOT loop, do NOT start a second experiment. A fresh agent will be spawned for the next experiment. Violating this rule wastes context and breaks the experiment loop.
- **Stay within the time budget.** If evaluation takes more than 60 seconds, the strategy is too slow. Optimize the heuristic, don't just add more search depth.
- **Push after every keep/discard decision.** Use `git push -u origin autoresearch`.
