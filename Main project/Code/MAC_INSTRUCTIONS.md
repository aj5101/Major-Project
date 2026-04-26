# 🍎 Mac Instructions for AI Lesson Generation

## 🚀 Step-by-Step Guide

### 1. Open Browser
- Use **Chrome** (recommended) or **Safari**
- Navigate to: `http://localhost:3001/create-lesson`

### 2. Create AI Lesson
1. **Title**: Enter "Hello Learn Together"
2. **Text**: Enter "Hello learn together"
3. **Click**: "🤖 Generate AI ASL Lesson" button
4. **Wait**: 5-10 seconds for generation

### 3. View Results
- You should see the AI-generated lesson
- Video should play automatically
- Look for "🤖 AI Generated" badge

### 4. If Issues Occur

#### Check Console Errors:
- **Chrome**: `Cmd + Option + I` → Console tab
- **Safari**: `Cmd + Option + C` → Console tab

#### Clear Cache:
- **Chrome**: `Cmd + Shift + Delete` → Clear browsing data
- **Safari**: `Cmd + Option + E` → Clear history

#### Try Different Browser:
- If Safari doesn't work, try Chrome
- If Chrome doesn't work, try Firefox

### 5. Test Video Directly
Open this URL in browser:
`http://127.0.0.1:8000/storage/processed/dynamic/custom_3dfee5e9.mp4`

If video plays → Issue is in React component
If video doesn't play → Issue is with server

### 6. Server Status Check
Both servers should be running:
- **Frontend**: `http://localhost:3001` (shows homepage)
- **Backend**: `http://127.0.0.1:8000/api/ai-status` (shows JSON response)

## 🔧 Troubleshooting

### Blank Page Solutions:
1. **Hard Refresh**: `Cmd + Shift + R`
2. **Clear Cache**: `Cmd + Shift + Delete`
3. **Check Console**: Look for red error messages
4. **Try Incognito**: Open in incognito/private window

### Network Error Solutions:
1. **Check Both Servers**: Make sure frontend (3001) and backend (8000) are running
2. **Wait 10 Seconds**: Let servers fully start
3. **Restart Browser**: Close and reopen browser

## ✅ Working Example

### Expected Flow:
1. Visit: `http://localhost:3001/create-lesson`
2. Enter: "Hello learn together"
3. Click: "🤖 Generate AI ASL Lesson"
4. See: AI-processed sentences + working video

### Expected Results:
- 🎓 Lesson: "Hello Learn Together"
- 📚 Sentences: "Hello" + "Learn together"
- 🤖 Badge: "AI Generated"
- 🎥 Video: 6-second ASL video

## 🎯 Quick Test

If direct URLs don't work, always use the **Create Lesson page** first:
`http://localhost:3001/create-lesson`

This ensures proper React state is passed to the lesson page.
