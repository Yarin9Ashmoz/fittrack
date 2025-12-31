#!/bin/bash

# Configuration
PORT=5001

echo "🔍 Checking for existing processes on port $PORT..."
# Find PID of process listening on the port
PID=$(lsof -t -i:$PORT)

if [ -n "$PID" ]; then
    echo "⚠️ Port $PORT is occupied by PID(s): $PID. Cleaning up..."
    # Kill all processes found on that port
    kill -9 $PID
    sleep 1
    echo "✅ Port $PORT is now available."
else
    echo "✅ Port $PORT is free."
fi

echo "🚀 Starting Fittrack Backend on http://127.0.0.1:$PORT..."

# Activate virtual environment
source backend/venv/bin/activate

# Use PYTHONPATH=. so python can find the 'backend' package
PYTHONPATH=. python3 -m backend.app
