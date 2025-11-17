#!/bin/bash

# Set the path to the log file we want to watch
LOG_FILE="logs/chat.log"

# Check if the log file exists
if [ ! -f $LOG_FILE ]; then
    # If it doesn't exist, create an empty one so tail doesn't fail
    echo "Log file not found, creating it: $LOG_FILE"
    touch $LOG_FILE
fi

echo "--- Live Log Monitor Started ---"
echo "Watching $LOG_FILE for 'WARNING' or 'Failed'..."
echo "----------------------------------------"

# This is the main command:
# 'tail -f' continuously watches the log file for new lines.
# '|' (pipe) sends every new line from 'tail' over to 'grep'.
# 'grep' filters the lines, only printing ones that contain 'WARNING' or 'Failed'.
tail -f $LOG_FILE | grep --line-buffered --color=always -E 'WARNING|Failed'
