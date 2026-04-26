#!/bin/bash

# Setup script for ASL Narration Platform
# This script sets up the development environment

set -e

echo "🚀 Setting up ASL Narration Platform..."

# Create storage directories
echo "📁 Creating storage directories..."
mkdir -p storage/videos
mkdir -p storage/asl_clips
mkdir -p storage/processed
mkdir -p storage/embeddings
mkdir -p datasets

# Backend setup
echo "🐍 Setting up Python backend..."
cd backend
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
cd ..

# Frontend setup
echo "📦 Setting up Node.js frontend..."
cd frontend
if [ ! -d "node_modules" ]; then
    npm install
fi
cd ..

# Database setup
echo "🗄️  Setting up database..."
echo "Please ensure PostgreSQL is running and create the database:"
echo "  createdb asl_narration"
echo ""
echo "Or use Docker Compose:"
echo "  docker-compose up -d postgres"

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Set up PostgreSQL database"
echo "2. Configure .env file in backend/"
echo "3. Run backend: cd backend && source venv/bin/activate && python -m app.main"
echo "4. Run frontend: cd frontend && npm run dev"
echo "5. Import ASL dataset using dataset_preprocessing/process_asl_videos.py"

