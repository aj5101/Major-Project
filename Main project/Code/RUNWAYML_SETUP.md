# 🎬 RunwayML Gen-2 AI Video Generation Setup

## 🚀 Getting Started with RunwayML Gen-2

### **1. Get Your RunwayML API Key**

1. **Visit**: https://runwayml.com/studio/api-keys
2. **Sign up** or **Log in** to your RunwayML account
3. **Click "Generate API Key"**
4. **Copy the key**: It will look like `rw_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
5. **Note your free tier**: ~125 seconds per month

### **2. Configure Your Environment**

Add your RunwayML API key to your backend `.env` file:

```env
# RunwayML Gen-2 AI Video Generation
RUNWAY_API_KEY=rw_your_actual_api_key_here
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

## 🎯 **Why RunwayML Gen-2?**

### **Superior Features:**
- ✅ **Professional Quality**: Hollywood-grade video generation
- ✅ **Generous Free Tier**: ~125 seconds/month (vs 10 seconds for others)
- ✅ **Educational Content**: Excellent for instructional videos
- ✅ **High Resolution**: Up to 4K quality
- ✅ **Fast Generation**: Usually 1-3 minutes
- ✅ **Reliable API**: Stable and well-documented

### **Perfect for ASL Lessons:**
- Clear hand gestures and movements
- Educational style prompts work well
- Professional appearance for classroom use
- Consistent quality across generations

## 🔧 **How It Works**

### **Generation Flow:**
1. **Text Input**: "Hello learn together"
2. **AI Processing**: Gemini AI simplifies to ASL-friendly format
3. **Video Generation**: RunwayML Gen-2 creates professional video
4. **Local Storage**: Video downloaded and stored locally
5. **Frontend Display**: High-quality video shown in lesson page

### **AI Video Prompts:**
The system creates optimized prompts like:
```
ASL sign language interpretation of: hello learn together. Clear hand gestures, educational content, simple background, professional quality, 4K resolution
```

## 📊 **Usage Examples**

### **Simple Lesson:**
```
Input: "The sun provides light and heat"
AI Output: "sun provides light heat"
RunwayML Video: 6-second professional ASL interpretation
```

### **Complex Lesson:**
```
Input: "Photosynthesis is the process by which plants convert light energy"
AI Output: "photosynthesis process plant take sun light"
RunwayML Video: 6-second educational ASL video with clear gestures
```

### **Educational Content:**
```
Input: "Water evaporates and forms clouds"
AI Output: "water evaporates forms clouds"
RunwayML Video: Professional weather education video with ASL interpretation
```

## ⚡ **Performance & Quality**

### **Generation Times:**
- **RunwayML Gen-2**: 1-3 minutes (professional quality)
- **Fallback System**: 5-10 seconds (existing clips)
- **Queue Priority**: Free tier users may experience short queues

### **Quality Comparison:**
- **RunwayML**: Professional, cinematic quality ASL gestures
- **Fallback**: Stitched existing sign clips
- **Recommendation**: Use RunwayML for final lessons, fallback for testing

### **Resolution Options:**
- **Default**: 1024x1024 (square format)
- **Quality**: Professional 4K-capable
- **Format**: MP4 for web compatibility

## 🎓 **Educational Benefits**

### **Why RunwayML for Education:**
1. **Professional Appearance**: Suitable for classroom presentations
2. **Clear Communication**: AI understands educational context
3. **Unlimited Vocabulary**: Generate any sign language concept
4. **Consistent Style**: Same professional look across all lessons
5. **Student Engagement**: High-quality videos maintain attention

### **Best Practices:**
1. **Simple Text**: 3-5 words per sentence works best
2. **Educational Focus**: Emphasize learning objectives
3. **Clear Concepts**: Use concrete, visual terms
4. **Quality Control**: Preview videos before classroom use
5. **Backup Planning**: Have fallback videos ready

## 🔍 **Troubleshooting**

### **Common Issues:**

#### "RUNWAY_API_KEY not found"
- **Solution**: Add API key to `.env` file
- **Check**: Ensure `.env` is in backend directory
- **Verify**: API key format should start with `rw_`

#### "Video generation failed"
- **Solution**: Check API key validity and remaining credits
- **Verify**: Visit https://runwayml.com/studio/api-keys
- **Monitor**: Check credit usage at RunwayML dashboard

#### "Generation timed out"
- **Solution**: Try shorter text or check server load
- **Alternative**: System falls back to existing video generation
- **Tip**: Free tier may have queue times during peak hours

#### "Insufficient credits"
- **Solution**: Wait for monthly reset or upgrade plan
- **Monitor**: Check credit balance regularly
- **Alternative**: Use fallback system when credits are low

### **API Limits:**
- **Free Tier**: ~125 seconds per month
- **Credit Usage**: 1 credit per second of video
- **Reset**: Monthly on subscription anniversary
- **Monitoring**: Available in RunwayML dashboard

## 🎯 **Testing**

### **Quick Test:**
```bash
curl -X POST "http://127.0.0.1:8000/api/generate-asl-lesson" \
  -H "Content-Type: application/json" \
  -d '{
    "lesson_title": "RunwayML Test",
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
    "ai_generated": true,
    "duration": 6
  },
  "message": "AI lesson and video generated successfully!"
}
```

### **Quality Verification:**
1. **Check Video**: Ensure clear ASL gestures
2. **Audio**: Verify no unwanted audio
3. **Duration**: Confirm correct length
4. **Resolution**: Professional quality expected

## 🚀 **Production Deployment**

### **For Classroom Use:**
1. **Test Generation**: Always preview videos before showing students
2. **Credit Management**: Monitor monthly usage carefully
3. **Backup System**: Keep fallback videos ready
4. **Quality Standards**: Review all AI-generated content

### **Cost Management:**
1. **Free Tier**: Excellent for small classes and testing
2. **Credit Planning**: Budget ~125 seconds per month
3. **Hybrid Approach**: Use RunwayML for important lessons
4. **Usage Tracking**: Monitor consumption regularly

### **Scaling Considerations:**
1. **Multiple Classes**: May need paid plan for higher usage
2. **Content Library**: Generate and store reusable videos
3. **Queue Management**: Plan for peak usage times
4. **Quality Standards**: Maintain professional appearance

## 🎉 **Ready to Use!**

### **Complete Setup Checklist:**
- [ ] RunwayML account created
- [ ] API key obtained
- [ ] `.env` file configured
- [ ] Backend server restarted
- [ ] Frontend accessible
- [ ] Test generation successful

### **Generate Your First AI Video:**
1. **Visit**: http://localhost:3001/create-lesson
2. **Enter**: "Hello learn together"
3. **Click**: "🤖 Generate AI ASL Lesson"
4. **Wait**: 1-3 minutes for professional video generation
5. **Enjoy**: High-quality ASL lesson with RunwayML video!

## 🎬 **Advanced Features**

### **Custom Prompts:**
The system can be customized for specific educational contexts:
- **Science Lessons**: Focus on scientific concepts
- **Math Lessons**: Emphasize numerical concepts
- **Language Arts**: Focus on storytelling elements

### **Quality Settings:**
- **Resolution**: Up to 4K for professional use
- **Duration**: Adjustable from 3-10 seconds
- **Style**: Educational, professional, or casual
- **Background**: Simple or contextual

### **Integration Benefits:**
- **Seamless Workflow**: Integrated with existing ASL system
- **Fallback Support**: Always functional, even without credits
- **Professional Output**: Suitable for educational institutions
- **Scalable Solution**: Works for individual lessons or curricula

**🎓 Your AI-powered ASL lesson generation system is now ready with professional RunwayML Gen-2 video integration!**

### **Next Steps:**
1. **Test the system** with simple lessons
2. **Monitor credit usage** for planning
3. **Create a content library** of reusable videos
4. **Scale up** based on classroom needs

**Enjoy professional-quality AI-generated ASL videos for your educational content!** 🎬✨
