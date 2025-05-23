#!/bin/bash
# start_server.sh - Script to easily start the HTTP file server
#
# Usage: 
#   ./start_server.sh                    # Start with default settings (port 8000, 'uploads' folder)
#   ./start_server.sh 9000               # Start with custom port 9000 and default 'uploads' folder
#   ./start_server.sh 8080 /data/files   # Start with custom port and directory
#

# Set default values
PORT=8000
# Default directory will be handled by the Python script (uploads folder)
DIR=""

# Check for custom port argument
if [ ! -z "$1" ]; then
    PORT="$1"
fi

# Check for custom directory argument
if [ ! -z "$2" ]; then
    DIR="--directory $2"
fi

# Print banner
echo "═══════════════════════════════════════════"
echo "       HTTP FILE SERVER STARTER"
echo "═══════════════════════════════════════════"
echo "Starting server with:"
echo "- Port: $PORT"
echo "- Directory: ${DIR:-'Default (uploads folder)'}"
echo "═══════════════════════════════════════════"

# Run the file server with the specified parameters
python3 "$(dirname "$0")/file_server.py" --port "$PORT" $DIR
