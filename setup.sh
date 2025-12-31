#!/bin/bash

echo "🚀 Setting up Fittrack Backend..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Navigate to backend directory
cd backend

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Configure backend/config.ini with your MySQL credentials"
echo "  2. Run './init_db.sh' to create database tables"
echo "  3. Run './run.sh' to start the application"
