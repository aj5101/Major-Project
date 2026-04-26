# AI Lesson Generation Setup Guide

## 🎯 Overview
The ASL Classroom Accessibility Platform now features AI-powered lesson generation using Google Gemini API. This guide will help you set up and configure the AI features.

## 🚀 Quick Setup

### 1. Get Google Gemini API Key
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy your API key

### 2. Configure Backend
```bash
cd backend
cp .env.example .env
```

Edit `.env` file:
```env
GEMINI_API_KEY=your_actual_api_key_here
```

### 3. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 4. Start Services
```bash
# Terminal 1: Start backend
cd backend
python -m app.main

# Terminal 2: Start frontend
cd frontend
npm run dev
```

## ✨ Features

### AI-Powered Lesson Generation
- **Smart Simplification**: Converts complex text to ASL-friendly grammar
- **Visual Word Mapping**: Selects words with common ASL signs
- **Sentence Breakdown**: Optimizes sentence length for signing
- **Fallback System**: Works even without AI using rule-based simplification

### User Interface
- **AI Status Indicator**: Shows if AI is available
- **Toggle Control**: Enable/disable AI generation
- **Enhanced UI**: Modern loading states and animations
- **Error Handling**: Graceful fallback when AI fails

## 🎮 Usage

1. Navigate to `/create-lesson` in the frontend
2. Enter lesson title and content
3. Click "🤖 Generate AI ASL Lesson"
4. View AI-processed sentences and ASL sequences
5. Generated video combines all ASL signs

## 📊 API Endpoints

### Generate ASL Lesson
```http
POST /api/generate-asl-lesson
Content-Type: application/json

{
  "lesson_title": "Water Cycle",
  "lesson_text": "Water evaporates from the surface...",
  "use_ai": true
}
```

### AI Status Check
```http
GET /api/ai-status
```

### Preview Lesson (No Video)
```http
POST /api/preview-lesson
Content-Type: application/json

{
  "lesson_title": "Water Cycle",
  "lesson_text": "Water evaporates..."
}
```

## 🔄 Fallback System

When AI is unavailable, the system automatically uses rule-based simplification:
- Removes filler words (articles, helping verbs)
- Limits sentences to 5 words
- Extracts key vocabulary for ASL
- Maintains educational value

## 🎯 Example Output

### Input
```
"Water evaporates from the surface when heated by the sun."
```

### AI Output
```json
{
  "lesson_title": "Water Cycle",
  "sentences": [
    {
      "original": "Water evaporates from the surface when heated by the sun",
      "simplified": "water evaporate surface sun",
      "asl_sequence": ["water", "evaporate", "surface", "sun"]
    }
  ]
}
```

### Fallback Output
```json
{
  "lesson_title": "Water Cycle",
  "sentences": [
    {
      "original": "Water evaporates from the surface when heated by the sun",
      "simplified": "water evaporates from surface when",
      "asl_sequence": ["water", "evaporates", "from", "surface"]
    }
  ],
  "fallback_used": true
}
```

## 🧪 Testing

Run the comprehensive test suite:
```bash
python test_ai_lesson_flow.py
```

## 📁 File Structure

```
backend/
├── app/
│   ├── services/
│   │   └── ai_lesson_service.py      # AI service implementation
│   └── routes/
│       └── ai_lesson.py            # API endpoints
├── .env.example                     # Environment template
└── requirements.txt                 # Dependencies

frontend/
├── src/
│   ├── services/
│   │   └── api.js                   # Updated with AI API calls
│   └── pages/
│       └── CreateLesson.jsx         # Enhanced UI with AI features
└── .env.example                     # Environment template

test_ai_lesson_flow.py               # Comprehensive test suite
```

## 🔧 Configuration Options

### Environment Variables
- `GEMINI_API_KEY`: Google Gemini API key
- `AI_MODEL`: Model name (default: gemini-pro)
- `AI_TEMPERATURE`: Creativity level (0.0-1.0)
- `AI_MAX_TOKENS`: Response length limit

### AI Prompt Customization
Edit `ai_lesson_service.py` to modify:
- Prompt templates
- ASL word mappings
- Simplification rules
- Output format

## 🚨 Troubleshooting

### AI Not Available
- Check API key in `.env`
- Verify internet connection
- Check API quota limits

### Video Generation Issues
- Ensure ASL video clips exist in `storage/asl_clips/`
- Check file permissions
- Verify moviepy installation

### Frontend Issues
- Check API URL in `.env`
- Verify CORS settings
- Check browser console for errors

## 🎉 Success Indicators

✅ **AI Available**: Green status indicator in UI  
✅ **AI Generation**: "🤖 AI Generation Active" message  
✅ **Fallback Mode**: "🔄 Using Rule-Based Generation"  
✅ **Video Created**: ASL video generated successfully  
✅ **Complete Flow**: All tests pass  

## 📞 Support

For issues:
1. Check test output: `python test_ai_lesson_flow.py`
2. Verify environment setup
3. Check API key validity
4. Review logs in backend console

---

**🎓 Ready to transform lessons with AI-powered ASL generation!**
