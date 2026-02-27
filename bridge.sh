#!/bin/bash
# bridge.sh - Send a message to Codex and capture its response
# Usage: ./bridge.sh "your message here"

CODEX_PANE="${CODEX_PANE:-main:0.0}"
TIMEOUT="${TIMEOUT:-90}"
MESSAGE="$*"

if [ -z "$MESSAGE" ]; then
    echo "Usage: bridge.sh <message>" >&2
    exit 1
fi

# Send message to Codex (text first, then Enter separately)
tmux send-keys -t "$CODEX_PANE" "$MESSAGE"
sleep 0.2
tmux send-keys -t "$CODEX_PANE" "" Enter

echo "[Claude → Codex]: $MESSAGE" >&2

# Wait for Codex to start processing
sleep 2

# Poll until "Working" indicator disappears
for i in $(seq 1 "$TIMEOUT"); do
    if ! tmux capture-pane -t "$CODEX_PANE" -p | grep -q "• Working"; then
        break
    fi
    if [ "$i" -eq "$TIMEOUT" ]; then
        echo "[bridge]: Timeout waiting for Codex response" >&2
        exit 1
    fi
    sleep 1
done

sleep 0.5

# Extract Codex's response: text between our message and the next prompt
tmux capture-pane -t "$CODEX_PANE" -p -S -500 | \
    awk -v msg="${MESSAGE:0:40}" '
        index($0, msg) { found=1; next }
        found && /^›/ { exit }
        found && NF { print }
    '
