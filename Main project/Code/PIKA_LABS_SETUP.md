# 🎥 Pika Labs AI Video Generation Setup

## 🚀 Getting Started with Pika Labs

### **1. Get Your Pika Labs API Key**

1. **Visit**: https://pika.art
2. **Sign up** for a free account
3. **Go to API Settings**: Click on your profile → API Keys
4. **Generate API Key**: Click "Create New Key"
5. **Copy the key**: It will look like `pk_live_...`

### **2. Configure Your Environment**

Add your Pika Labs API key to your backend `.env` file:

```env
# Pika Labs AI Video Generation
PIKA_API_KEY=pk_live_your_actual_api_key_here
```

### **3. Install Dependencies**

```bash
cd backend
pip install -r requirements.txt
```

### **4. Restart Backend Server**

```bash
cd backend
python -m app.main
```

## 🎯 **Features**

### **What Pika Labs Provides:**
- ✅ **Free Tier**: ~10 seconds of video generation per month
- ✅ **Text-to-Video**: Convert text directly to video
- ✅ **Educational Content**: Perfect for ASL lessons
- ✅ **High Quality**: 512x512 resolution, good for web
- ✅ **Fast Generation**: Usually completes in 1-3 minutes

### **AI Video Prompts:**
The system automatically creates optimized prompts like:
```
ASL sign language interpretation: hello learn together. Clear hand gestures, educational style, simple background, high quality, 4K
```

## 🔧 **How It Works**

### **Generation Flow:**
1. **Text Input**: "Hello learn together"
2. **AI Processing**: Gemini AI simplifies to ASL-friendly format
3. **Video Generation**: Pika Labs creates video from simplified text
4. **Local Storage**: Video downloaded and stored locally
5. **Frontend Display**: Video shown in lesson page

### **Fallback System:**
If Pika Labs is unavailable:
- Falls back to existing video generation system
- Still provides functional ASL lessons
- No interruption to service

## 📊 **Usage Examples**

### **Simple Lesson:**
```
Input: "The sun provides light and heat"
AI Output: "sun provides light heat"
Video: 6-second ASL interpretation video
```

### **Complex Lesson:**
```
Input: "Photosynthesis is the process by which plants convert light energy"
AI Output: "photosynthesis process plant take sun light"
Video: 6-second educational ASL video
```

## ⚡ **Performance**

### **Generation Times:**
- **Pika Labs**: 1-3 minutes (high quality)
- **Fallback**: 5-10 seconds (existing system)
- **Queue Time**: Varies based on demand

### **Quality Comparison:**
- **Pika Labs**: AI-generated sign language gestures
- **Fallback**: Stitched existing sign clips
- **Recommendation**: Use Pika Labs for new content, fallback for testing

## 🎓 **Educational Benefits**

### **Why AI Video Generation:**
1. **Unlimited Vocabulary**: Not limited by existing sign clips
2. **Context-Aware**: AI understands educational context
3. **Consistent Quality**: Same style across all lessons
4. **Scalable**: Generate unlimited lessons

### **Best Practices:**
1. **Simple Text**: 3-5 words per sentence works best
2. **Clear Concepts**: Use concrete, visual terms
3. **Educational Focus**: Prioritize learning objectives
4. **Regular Testing**: Verify video quality before classroom use

## 🔍 **Troubleshooting**

### **Common Issues:**

#### "PIKA_API_KEY not found"
- **Solution**: Add API key to `.env` file
- **Check**: Make sure `.env` is in backend directory

#### "Video generation failed"
- **Solution**: Check API key validity and quota
- **Verify**: Visit pika.art to check account status

#### "Generation timed out"
- **Solution**: Try shorter text or check server load
- **Alternative**: System falls back to existing video generation

#### "Poor video quality"
- **Solution**: Adjust prompt or try different wording
- **Tip**: Use simple, concrete terms

### **API Limits:**
- **Free Tier**: ~10 seconds per month
- **Paid Plans**: Available for higher usage
- **Monitoring**: Check usage at pika.art/dashboard

## 🎯 **Testing**

### **Quick Test:**
```bash
curl -X POST "http://127.0.0.1:8000/api/generate-asl-lesson" \
  -H "Content-Type: application/json" \
  -d '{
    "lesson_title": "Pika Test",
    "lesson_text": "Hello learn together",
    "use_ai": true
  }'
```

### **Expected Response:**
```json
{
  "success": true,
  "lesson_data": {...},
  "video_data": {
    "video_file": "ai_video_abc12345.mp4",
    "ai_generated": true
  },
  "message": "AI lesson and video generated successfully!"
}
```

## 🚀 **Production Tips**

### **For Classroom Use:**
1. **Test First**: Always preview videos before showing students
2. **Have Backup**: Keep fallback videos ready
3. **Monitor Usage**: Track API quota consumption
4. **Quality Control**: Review AI-generated content

### **Cost Management:**
1. **Free Tier**: Great for testing and small classes
2. **Paid Plans**: Consider for larger deployments
3. **Hybrid Approach**: Use AI for new content, fallback for review

## 🎉 **Ready to Use!**

Once configured:
1. **Visit**: http://localhost:3001/create-lesson
2. **Enter**: Your lesson text
3. **Click**: "🤖 Generate AI ASL Lesson"
4. **Wait**: 1-3 minutes for AI video generation
5. **Enjoy**: High-quality ASL lesson with AI-generated video!

**🎓 Your AI-powered ASL lesson generation system is now ready with Pika Labs video integration!**
