#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <NEW_NETWORK>"
    exit 1
fi

NEW_NETWORK="$1"

TARGET_VARIABLE=NETWORK_NAME

# Function to update the variable recursively
update_variable() {
    local file="$1"
    if [ -f "$file" ]; then
        # Update variable in files
        sed -i "s/$TARGET_VARIABLE=.*-network/$TARGET_VARIABLE=$NEW_NETWORK/g" \
            "$file" | sed 's/^\([^=]*="\| *\)/\1/'
    elif [ -d "$file" ]; then
        # Recursively update variable in subdirectories
        for f in "$file"/*; do
            update_variable "$f"
        done
    fi
}

# Start updating from the current directory
update_variable .. 2>/dev/null

echo "$TARGET_VARIABLE has been updated to '$NEW_NETWORK'."
