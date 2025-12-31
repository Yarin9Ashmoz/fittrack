#!/bin/bash

echo "🌱 Seeding Fittrack Database..."

# Activate virtual environment
source backend/venv/bin/activate

# Set Python path and run seed script
cd backend
PYTHONPATH=.. python -m backend.scripts.seed_db

echo "✅ Database seeded with sample data!"
echo ""
echo "Sample users created:"
echo "  Admin:   yossi@example.com"
echo "  Trainer: sara@example.com"  
echo "  Member:  michal@example.com"
