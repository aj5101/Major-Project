# How to Run the ASL Narration Platform

## 🚀 Quick Start (Step-by-Step)

### Step 1: Check Prerequisites

Make sure you have these installed:
```bash
# Check Python (need 3.9+)
python3 --version

# Check Node.js (need 18+)
node --version

# Check PostgreSQL (or use Docker)
psql --version
# OR use Docker: docker --version
```

### Step 2: Initial Setup

Run the setup script to install dependencies:
```bash
cd "/Users/arihantjain/Desktop/final major project"
chmod +x setup.sh
./setup.sh
```

**OR manually:**

```bash
# Create virtual environment for backend
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cd ..

# Install frontend dependencies
cd frontend
npm install
cd ..
```

### Step 3: Set Up Database

**Option A: Using Docker (Easiest)**
```bash
docker-compose up -d postgres
```

**Option B: Local PostgreSQL**
```bash
# Create database
createdb asl_narration

# Or using psql:
psql -U postgres -c "CREATE DATABASE asl_narration;"
```

### Step 4: Configure Environment Variables

Create `backend/.env` file:
```bash
cd backend
cat > .env << EOF
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
cd ..
```

### Step 5: Start Backend Server

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
python -m app.main
```

You should see:
```
INFO:     Started server process
INFO:     Waiting for application startup.
Database tables initialized
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

✅ Backend is running at: **http://localhost:8000**

### Step 6: Start Frontend Server

**Terminal 2 - Frontend (Open a NEW terminal):**
```bash
cd "/Users/arihantjain/Desktop/final major project/frontend"
npm run dev
```

You should see:
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:3000/
```

✅ Frontend is running at: **http://localhost:3000**

### Step 7: (Optional) Import ASL Dataset

Before processing videos, you need ASL video clips in the dataset:

```bash
# If you have WLASL or other ASL dataset:
python dataset_preprocessing/process_asl_videos.py \
    --dataset_path datasets/wlasl

# Or add videos manually via Admin panel at http://localhost:3000/admin
```

### Step 8: Test the Application!

1. **Open browser:** http://localhost:3000
2. **Click:** "📤 Upload Video"
3. **Upload:** A video file with spoken words (MP4, AVI, MOV, etc.)
4. **Wait:** Processing takes a few minutes
5. **View:** Your ASL narration result!

## 🐳 Alternative: Run Everything with Docker

If you prefer Docker:

```bash
# Start all services (PostgreSQL + Backend + Frontend)
docker-compose up

# Or run in background:
docker-compose up -d

# View logs:
docker-compose logs -f

# Stop everything:
docker-compose down
```

## 📋 Complete Command Reference

### Start Backend
```bash
cd backend
source venv/bin/activate
python -m app.main
# OR: uvicorn app.main:app --reload
```

### Start Frontend
```bash
cd frontend
npm run dev
```

### Check Backend Health
```bash
curl http://localhost:8000/api/health
```

### View API Documentation
Open in browser: http://localhost:8000/docs

### Import ASL Dataset
```bash
python dataset_preprocessing/process_asl_videos.py \
    --dataset_path /path/to/asl/videos \
    --gloss_file /path/to/gloss_mapping.json
```

### Regenerate Embeddings
```bash
cd backend
source venv/bin/activate
python ../dataset_preprocessing/generate_embeddings.py
```

## 🔧 Troubleshooting

### Backend Issues

**Port 8000 already in use:**
```bash
# Change port in backend/.env:
PORT=8001
```

**Database connection error:**
```bash
# Check PostgreSQL is running:
pg_isready

# Check database exists:
psql -l | grep asl_narration

# Create if missing:
createdb asl_narration
```

**Module not found errors:**
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

### Frontend Issues

**Port 3000 already in use:**
```bash
# Change port in frontend/vite.config.js
server: { port: 3001 }
```

**npm install fails:**
```bash
# Clear cache and retry:
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

**API connection error:**
- Check backend is running on port 8000
- Check CORS_ORIGINS in backend/.env includes http://localhost:3000

### Processing Issues

**No ASL clips found:**
- Import ASL dataset first
- Check storage/asl_clips/ has video files
- Regenerate embeddings

**FFmpeg not found:**
```bash
# macOS:
brew install ffmpeg

# Ubuntu/Debian:
sudo apt-get install ffmpeg

# Windows: Download from https://ffmpeg.org/
```

**Whisper model download slow:**
- First run downloads the model (~150MB for 'base')
- Be patient, it only downloads once
- Check internet connection

## 📊 Verify Everything Works

1. **Backend API:** http://localhost:8000/api/health
   - Should return: `{"status":"healthy",...}`

2. **Frontend:** http://localhost:3000
   - Should show homepage with navigation

3. **API Docs:** http://localhost:8000/docs
   - Should show Swagger UI

4. **Database:**
   ```bash
   psql -d asl_narration -c "SELECT COUNT(*) FROM videos;"
   ```

## 🎯 Next Steps

- Upload a test video
- Add ASL videos via Admin panel
- Customize text simplification
- Read ARCHITECTURE.md for system details

---

**Need help?** Check the main README.md for detailed documentation!

