#!/bin/bash

# Configuration
PORT=3000

echo "🔍 Checking for existing processes on port $PORT..."
PID=$(lsof -t -i:$PORT)

if [ -n "$PID" ]; then
    echo "⚠️ Port $PORT is occupied. Cleaning up..."
    kill -9 $PID
    sleep 1
fi

echo "🚀 Starting Fittrack Frontend on http://127.0.0.1:$PORT..."

cd frontend
npm run dev
