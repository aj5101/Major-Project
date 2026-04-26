# Architecture Documentation

## System Architecture

### High-Level Overview

The platform follows a three-tier architecture:

1. **Presentation Layer (Frontend)**
   - React.js SPA with Tailwind CSS
   - Accessible, child-friendly UI
   - Real-time status updates via polling

2. **Application Layer (Backend)**
   - FastAPI REST API
   - Business logic and orchestration
   - Background task processing

3. **Data Layer**
   - PostgreSQL for metadata
   - File system for video storage
   - FAISS for vector search

## Data Flow

### Video Processing Pipeline

```
User Uploads Video
    ↓
Backend saves video file
    ↓
Background task starts
    ↓
[Step 1] Extract audio → Whisper STT → Text
    ↓
[Step 2] Text Simplification → Simplified Text
    ↓
[Step 3] Break into phrases
    ↓
[Step 4] For each phrase:
    - Generate text embedding
    - Search FAISS index
    - Retrieve best ASL clip
    ↓
[Step 5] Stitch ASL clips → Final video
    ↓
Save result → Update database
    ↓
User views result
```

## Component Details

### Backend Components

#### 1. API Routes (`app/routes/`)
- **video.py**: Video upload, processing, results
- **asl_dataset.py**: ASL dataset management
- **health.py**: Health checks

#### 2. Services (`app/services/`)
- **video_service.py**: Video file operations
- **processing_service.py**: Orchestrates ML pipeline
- **asl_dataset_service.py**: ASL dataset operations

#### 3. Models (`app/models/`)
- **db_models.py**: SQLAlchemy ORM models
- **schemas.py**: Pydantic validation schemas
- **database.py**: Database connection

### ML Pipeline Components

#### 1. Speech-to-Text (`ml_pipeline/speech_to_text.py`)
- Uses OpenAI Whisper
- Extracts audio from video
- Returns transcribed text

#### 2. Text Simplification (`ml_pipeline/text_simplification.py`)
- Rule-based vocabulary replacement
- Sentence length reduction
- Age-appropriate simplification

#### 3. ASL Retrieval (`ml_pipeline/asl_retrieval.py`)
- Sentence transformer embeddings
- FAISS vector similarity search
- Fallback keyword matching

#### 4. Video Processing (`ml_pipeline/video_processing.py`)
- Video normalization
- Clip concatenation
- Final video generation

### Frontend Components

#### 1. Pages (`src/pages/`)
- **HomePage**: Landing page with recent videos
- **VideoUploadPage**: Upload interface
- **VideoResultPage**: Results display
- **AdminPage**: Dataset management

#### 2. Components (`src/components/`)
- **Navbar**: Navigation bar

#### 3. Services (`src/services/`)
- **api.js**: API client with error handling

## Database Schema

### Tables

1. **videos**
   - Stores uploaded videos
   - Tracks processing status
   - Links to ASL clips

2. **asl_video_dataset**
   - Stores ASL video clips
   - Metadata (gloss, duration, path)
   - Embedding paths

3. **video_asl_clips**
   - Junction table
   - Links videos to ASL clips
   - Stores timing and sequence

## Storage Structure

```
storage/
├── videos/          # Uploaded videos
├── asl_clips/      # ASL video dataset
├── processed/       # Generated ASL narrations
└── embeddings/     # Video embeddings (.npy files)
```

## API Design

### RESTful Endpoints

- `POST /api/videos/upload` - Upload video
- `POST /api/videos/{id}/process` - Start processing
- `GET /api/videos/{id}/status` - Get status
- `GET /api/videos/{id}/result` - Get result
- `GET /api/videos/{id}/asl-video` - Stream video
- `GET /api/asl-dataset/` - List ASL videos
- `POST /api/asl-dataset/` - Add ASL video
- `DELETE /api/asl-dataset/{id}` - Delete ASL video

### Response Formats

All responses use JSON except video streaming.

Error responses:
```json
{
  "message": "Error description",
  "error": "Detailed error (optional)"
}
```

## Security Considerations

1. **File Upload Validation**
   - File type checking
   - File size limits
   - Path sanitization

2. **Database Security**
   - Parameterized queries (SQLAlchemy)
   - Input validation (Pydantic)

3. **CORS Configuration**
   - Restricted origins
   - Credential handling

## Performance Optimizations

1. **Background Processing**
   - Async task processing
   - Non-blocking API responses

2. **Vector Search**
   - FAISS for fast similarity search
   - Pre-computed embeddings
   - Index caching

3. **Video Processing**
   - Efficient video codecs
   - Resolution normalization
   - Streaming for large files

## Scalability Considerations

1. **Horizontal Scaling**
   - Stateless API design
   - Shared database
   - Distributed storage

2. **Caching**
   - Embedding cache
   - FAISS index caching
   - Result caching

3. **Queue System** (Future)
   - Redis/Celery for task queue
   - Priority queues
   - Retry mechanisms

## Monitoring and Logging

- Application logs for debugging
- Processing status tracking
- Error logging and reporting

## Deployment Architecture

### Development
- Local PostgreSQL
- Local file storage
- Development servers

### Production (Recommended)
- Containerized services (Docker)
- Cloud database (AWS RDS, etc.)
- Object storage (S3, etc.)
- Load balancer
- CDN for static assets

