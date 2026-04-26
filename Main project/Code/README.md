# Video Narration Platform for Hearing-Impaired Children Using Real ASL Video Data

A complete, production-ready platform that converts spoken video/audio content into accessible American Sign Language (ASL) narration using real ASL video datasets. Designed specifically for hearing-impaired children with a simple, visual-first interface.

## 🎯 Project Overview

This platform enables hearing-impaired children to access video content through ASL narration by:
1. Extracting speech from uploaded videos
2. Converting speech to text using OpenAI Whisper
3. Simplifying text for children (ages 6-12)
4. Retrieving matching ASL video clips from a real dataset
5. Stitching clips together to create a complete ASL narration
6. Displaying both original and ASL videos side-by-side

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend (React)                      │
│  - Upload Interface  - Video Player  - Admin Panel           │
└───────────────────────┬───────────────────────────────────────┘
                        │ HTTP/REST API
┌───────────────────────▼───────────────────────────────────────┐
│                    Backend (FastAPI)                          │
│  - Video Upload  - Processing Queue  - ASL Dataset Management  │
└───────────────────────┬───────────────────────────────────────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
┌───────▼──────┐ ┌──────▼──────┐ ┌─────▼──────┐
│ ML Pipeline  │ │  Database   │ │  Storage   │
│              │ │ (PostgreSQL) │ │  (Local)   │
│ - Whisper    │ │             │ │            │
│ - Text       │ │ - Videos    │ │ - Videos   │
│   Simplifier │ │ - ASL Clips │ │ - ASL Clips│
│ - ASL        │ │ - Metadata  │ │ - Embeddings│
│   Retrieval  │ │             │ │            │
│ - Video      │ │             │ │            │
│   Stitching  │ │             │ │            │
└──────────────┘ └─────────────┘ └────────────┘
```

## 📁 Project Structure

```
video-narration-asl/
├── backend/                    # FastAPI backend
│   ├── app/
│   │   ├── main.py            # FastAPI application entry point
│   │   ├── models/            # Database models and schemas
│   │   ├── routes/            # API route handlers
│   │   ├── services/          # Business logic services
│   │   └── utils/             # Utility functions
│   └── requirements.txt        # Python dependencies
│
├── frontend/                   # React frontend
│   ├── src/
│   │   ├── components/        # Reusable UI components
│   │   ├── pages/             # Page components
│   │   ├── services/          # API client
│   │   └── styles/            # CSS/Tailwind styles
│   └── package.json           # Node.js dependencies
│
├── ml_pipeline/               # ML processing modules
│   ├── speech_to_text.py      # Whisper STT
│   ├── text_simplification.py # Text simplification
│   ├── asl_retrieval.py       # ASL video retrieval (FAISS)
│   └── video_processing.py    # Video stitching
│
├── dataset_preprocessing/    # Dataset processing scripts
│   ├── process_asl_videos.py  # Import ASL videos
│   └── generate_embeddings.py # Generate embeddings
│
├── datasets/                  # ASL video datasets
│   └── README.md              # Dataset documentation
│
├── storage/                   # File storage
│   ├── videos/                # Uploaded videos
│   ├── asl_clips/             # ASL video clips
│   ├── processed/             # Generated ASL narrations
│   └── embeddings/            # Video embeddings
│
└── README.md                  # This file
```

## 🚀 Setup Instructions

### Prerequisites

- Python 3.9+
- Node.js 18+
- PostgreSQL 14+
- FFmpeg (for video processing)

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   Create a `.env` file in the `backend` directory:
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

5. **Set up PostgreSQL database:**
   ```bash
   createdb asl_narration
   ```

6. **Run the backend:**
   ```bash
   python -m app.main
   ```
   Or using uvicorn:
   ```bash
   uvicorn app.main:app --reload
   ```

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Run the development server:**
   ```bash
   npm run dev
   ```

   The frontend will be available at `http://localhost:3000`

### Dataset Setup

1. **Download ASL video dataset:**
   - Recommended: [WLASL Dataset](https://github.com/dxli94/WLASL)
   - Or use any ASL lexicon dataset with video files

2. **Process the dataset:**
   ```bash
   python dataset_preprocessing/process_asl_videos.py \
       --dataset_path datasets/wlasl \
       --gloss_file datasets/wlasl/gloss_mapping.json
   ```

3. **Generate embeddings (if needed):**
   ```bash
   python dataset_preprocessing/generate_embeddings.py
   ```

## 🎬 Usage

### For End Users

1. **Upload a video:**
   - Navigate to the Upload page
   - Select or drag-and-drop a video file
   - Click "Upload & Process"

2. **Wait for processing:**
   - The system will transcribe speech
   - Simplify text for children
   - Retrieve matching ASL clips
   - Stitch clips together

3. **View results:**
   - Watch original and ASL videos side-by-side
   - View simplified text and subtitles
   - See which ASL clips were used

### For Administrators

1. **Add ASL videos to dataset:**
   - Navigate to Admin panel
   - Click "Add ASL Video"
   - Provide gloss (sign name) and video file
   - System automatically generates embedding

2. **Manage dataset:**
   - View all ASL videos in dataset
   - Delete videos if needed
   - Regenerate embeddings if model is updated

## 🔧 Technical Details

### ML Pipeline

1. **Speech-to-Text (Whisper):**
   - Uses OpenAI Whisper model (configurable size)
   - Extracts audio from video
   - Transcribes to text with high accuracy

2. **Text Simplification:**
   - Rule-based vocabulary replacement
   - Sentence length reduction based on target age
   - Punctuation simplification
   - Clarity improvements

3. **ASL Retrieval:**
   - Uses sentence transformers for text encoding
   - FAISS for fast similarity search
   - Falls back to keyword matching if needed
   - Returns best-matching ASL video clips

4. **Video Stitching:**
   - Normalizes video resolution and FPS
   - Concatenates ASL clips in sequence
   - Generates final narration video

### Database Schema

- **videos**: Uploaded videos and processing status
- **asl_video_dataset**: ASL video clips with metadata
- **video_asl_clips**: Junction table linking videos to ASL clips

### API Endpoints

- `POST /api/videos/upload` - Upload video
- `POST /api/videos/{id}/process` - Start processing
- `GET /api/videos/{id}/status` - Get processing status
- `GET /api/videos/{id}/result` - Get narration result
- `GET /api/videos/{id}/asl-video` - Stream ASL video
- `GET /api/asl-dataset/` - List ASL videos
- `POST /api/asl-dataset/` - Add ASL video
- `DELETE /api/asl-dataset/{id}` - Delete ASL video

## 🎨 UI/UX Features

- **Accessible Design:**
  - WCAG-compliant color contrast
  - Large, clear buttons
  - Keyboard navigation support
  - Screen reader friendly

- **Child-Friendly:**
  - Simple, intuitive interface
  - Visual icons and emojis
  - Large text and buttons
  - Clear instructions

- **Visual Feedback:**
  - Processing progress indicators
  - Status messages
  - Error handling with clear messages

## ⚠️ Limitations

1. **ASL Coverage:**
   - Limited to ASL videos in dataset
   - May not have clips for all phrases
   - Quality depends on dataset size

2. **Text Simplification:**
   - Rule-based approach (not ML-powered)
   - May not handle all complex sentences
   - Vocabulary mapping is limited

3. **Video Quality:**
   - ASL clips may have varying quality
   - Stitching may have minor transitions
   - Resolution normalized to 640x480

4. **Processing Time:**
   - Depends on video length
   - Whisper transcription can be slow
   - Video stitching takes time

## 🔮 Future Improvements

1. **Enhanced Text Simplification:**
   - Use ML models for better simplification
   - Age-specific vocabulary databases
   - Context-aware simplification

2. **Better ASL Retrieval:**
   - Video-specific embedding models (CLIP, action recognition)
   - Multi-modal search (text + visual features)
   - Support for ASL grammar and sentence structure

3. **Real-time Processing:**
   - Streaming video processing
   - Progressive ASL video generation
   - Live transcription support

4. **Expanded Features:**
   - Multiple ASL dialects
   - Custom ASL video uploads
   - User preferences and history
   - Mobile app support

5. **Performance:**
   - GPU acceleration for ML models
   - Distributed processing
   - Caching and optimization

## 🤝 Contributing

This is a production-ready project suitable for:
- Portfolio/resume showcase
- Educational purposes
- Further development
- Deployment to production

## 📝 Ethical Considerations

1. **Accessibility:**
   - Designed specifically for hearing-impaired children
   - Prioritizes accessibility and usability
   - Uses real ASL data (not synthetic avatars)

2. **Data Privacy:**
   - Videos are stored locally
   - No external data sharing
   - User data can be deleted

3. **ASL Representation:**
   - Uses real ASL video data
   - Respects ASL as a language
   - Acknowledges limitations in coverage

4. **Children's Safety:**
   - Simple, safe interface
   - No external links or ads
   - Content filtering can be added

## 📄 License

This project is provided as-is for educational and portfolio purposes.

## 🙏 Acknowledgments

- OpenAI Whisper for speech recognition
- WLASL dataset contributors
- ASL community for language resources
- Open-source libraries and frameworks used

## 📞 Support

For issues or questions:
1. Check the documentation
2. Review error messages
3. Check database and storage paths
4. Verify all dependencies are installed

---

**Built with ❤️ for hearing-impaired children**

