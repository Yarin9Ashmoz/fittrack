#!/bin/bash

echo "🗄️  Initializing Fittrack Database..."

# Activate virtual environment
source backend/venv/bin/activate

# Set Python path and run init script
cd backend
PYTHONPATH=.. python -m backend.scripts.init_db

echo "✅ Database tables created successfully!"
