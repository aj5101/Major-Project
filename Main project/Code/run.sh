#!/bin/bash

# Quick run script for ASL Narration Platform
# This script helps you start the application

echo "🤟 ASL Narration Platform - Quick Start"
echo "========================================"
echo ""

# Check if .env exists
if [ ! -f "backend/.env" ]; then
    echo "⚠️  Creating backend/.env file..."
    cat > backend/.env << EOF
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/asl_narration
HOST=0.0.0.0
PORT=8000
CORS_ORIGINS=http://localhost:3000
VIDEO_STORAGE_PATH=../storage/videos
ASL_STORAGE_PATH=../storage/asl_clips
OUTPUT_STORAGE_PATH=../storage/processed
EMBEDDINGS_PATH=../storage/embeddings
WHISPER_MODEL=base
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
EOF
    echo "✅ Created backend/.env"
fi

# Check if virtual environment exists
if [ ! -d "backend/venv" ]; then
    echo "⚠️  Creating Python virtual environment..."
    cd backend
    python3 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    cd ..
    echo "✅ Backend dependencies installed"
fi

# Check if node_modules exists
if [ ! -d "frontend/node_modules" ]; then
    echo "⚠️  Installing frontend dependencies..."
    cd frontend
    npm install
    cd ..
    echo "✅ Frontend dependencies installed"
fi

echo ""
echo "📋 Setup Checklist:"
echo "  1. ✅ Python dependencies"
echo "  2. ✅ Frontend dependencies"
echo "  3. ✅ Environment file"
echo ""
echo "🚀 Starting services..."
echo ""
echo "Choose an option:"
echo "  1) Start Backend only"
echo "  2) Start Frontend only"
echo "  3) Start Both (requires 2 terminals)"
echo "  4) Start with Docker Compose (all services)"
echo ""
read -p "Enter choice (1-4): " choice

case $choice in
    1)
        echo ""
        echo "Starting Backend..."
        echo "Backend will be available at: http://localhost:8000"
        echo "API docs at: http://localhost:8000/docs"
        echo ""
        cd backend
        source venv/bin/activate
        python -m app.main
        ;;
    2)
        echo ""
        echo "Starting Frontend..."
        echo "Frontend will be available at: http://localhost:3000"
        echo ""
        cd frontend
        npm run dev
        ;;
    3)
        echo ""
        echo "⚠️  You need TWO terminals for this!"
        echo ""
        echo "Terminal 1 - Backend:"
        echo "  cd backend && source venv/bin/activate && python -m app.main"
        echo ""
        echo "Terminal 2 - Frontend:"
        echo "  cd frontend && npm run dev"
        echo ""
        echo "Starting Backend in this terminal..."
        cd backend
        source venv/bin/activate
        python -m app.main
        ;;
    4)
        echo ""
        echo "Starting with Docker Compose..."
        echo "This will start PostgreSQL, Backend, and Frontend"
        echo ""
        docker-compose up
        ;;
    *)
        echo "Invalid choice"
        exit 1
        ;;
esac

