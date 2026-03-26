#!/bin/bash
# 2048 Autoresearch wrapper script
# Spawns a fresh Haiku agent for each experiment.
# Stops automatically when TARGET_REACHED file exists.
#
# Unlike the website autoresearch, there's no deploy to wait for —
# evaluation runs locally via `python evaluate.py`. We only pause
# briefly between experiments so the output is readable.
#
# Usage: bash run.sh
#   To stop: Ctrl+C (or wait for target to be reached)

EXPERIMENT=1

while true; do
    # Check if target was already reached
    if [ -f TARGET_REACHED ]; then
        echo ""
        echo "=========================================="
        echo "  TARGET REACHED — stopping autoresearch"
        echo "  Final score: $(cat TARGET_REACHED)"
        echo "=========================================="
        exit 0
    fi

    echo ""
    echo "=========================================="
    echo "  EXPERIMENT $EXPERIMENT — $(date)"
    echo "=========================================="
    echo ""

    # --print streams text output to stdout
    # --verbose shows tool call activity so you can watch the agent work
    "$HOME/.local/bin/claude" \
        --model haiku \
        --dangerously-skip-permissions \
        --print \
        --verbose \
        "Read program.md and begin."

    echo ""
    echo "--- Agent exited. Next experiment in 10s... ---"
    sleep 10

    EXPERIMENT=$((EXPERIMENT + 1))
done
