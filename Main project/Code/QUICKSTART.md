# Quick Start Guide

Get the ASL Narration Platform running in 5 minutes!

## Prerequisites Check

- ✅ Python 3.9+ installed
- ✅ Node.js 18+ installed
- ✅ PostgreSQL 14+ installed (or Docker)
- ✅ FFmpeg installed

## Step 1: Clone and Setup

```bash
# Navigate to project directory
cd "final major project"

# Run setup script
./setup.sh
```

## Step 2: Database Setup

### Option A: Using Docker
```bash
docker-compose up -d postgres
```

### Option B: Local PostgreSQL
```bash
createdb asl_narration
```

## Step 3: Configure Environment

Create `backend/.env`:
```env
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
```

## Step 4: Start Backend

```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
python -m app.main
```

Backend will run at `http://localhost:8000`

## Step 5: Start Frontend

In a new terminal:
```bash
cd frontend
npm run dev
```

Frontend will run at `http://localhost:3000`

## Step 6: Import ASL Dataset (Optional but Recommended)

```bash
# Download WLASL or other ASL dataset
# Then process it:
python dataset_preprocessing/process_asl_videos.py \
    --dataset_path datasets/wlasl
```

## Step 7: Test It!

1. Open `http://localhost:3000`
2. Click "Upload Video"
3. Upload a video with spoken words
4. Wait for processing
5. View ASL narration!

## Troubleshooting

### Backend won't start
- Check PostgreSQL is running
- Verify DATABASE_URL in .env
- Check port 8000 is available

### Frontend won't start
- Run `npm install` in frontend directory
- Check port 3000 is available

### Processing fails
- Ensure ASL dataset is imported
- Check storage directories exist
- Verify FFmpeg is installed

### No ASL clips found
- Import ASL dataset first
- Check ASL videos are in storage/asl_clips
- Regenerate embeddings: `python dataset_preprocessing/generate_embeddings.py`

## Next Steps

- Read full [README.md](README.md) for detailed documentation
- Check [ARCHITECTURE.md](ARCHITECTURE.md) for system design
- Add more ASL videos via Admin panel
- Customize text simplification rules

Happy signing! 🤟

