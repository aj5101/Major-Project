#!/usr/bin/env python3
"""
AI Lesson Generation Demo
Showcase the complete AI-powered ASL lesson generation workflow
"""

import requests
import json
import time
from datetime import datetime

def print_section(title):
    print(f"\n{'='*60}")
    print(f"🎯 {title}")
    print('='*60)

def print_lesson_preview(lesson_data):
    """Print formatted lesson preview"""
    print(f"\n📚 LESSON: {lesson_data['lesson_title']}")
    print("-" * 40)
    
    for i, sentence in enumerate(lesson_data['sentences'], 1):
        print(f"\n📝 Sentence {i}:")
        print(f"   Original: {sentence['original']}")
        print(f"   ASL-Ready: {sentence['simplified']}")
        print(f"   Signs: {', '.join(sentence['asl_sequence'])}")

def demo_ai_lesson_generation():
    """Demo the AI lesson generation API"""
    print_section("AI LESSON GENERATION DEMO")
    
    api_base = "http://127.0.0.1:8000/api"
    
    # Demo lessons
    demo_lessons = [
        {
            "title": "Water Cycle",
            "text": "Water evaporates from the surface when heated by the sun. The water vapor rises and forms clouds in the atmosphere. When clouds become heavy, precipitation occurs and water returns to Earth."
        },
        {
            "title": "Photosynthesis",
            "text": "Plants use sunlight to make food. Leaves capture sunlight. Roots absorb water from soil. Plants produce oxygen for animals."
        },
        {
            "title": "Simple Math",
            "text": "Two plus two equals four. Numbers help us count. We can add and subtract. Math is useful every day."
        }
    ]
    
    for i, lesson in enumerate(demo_lessons, 1):
        print(f"\n🚀 Demo {i}: {lesson['title']}")
        print("-" * 40)
        
        # Generate lesson
        payload = {
            "lesson_title": lesson['title'],
            "lesson_text": lesson['text'],
            "use_ai": True
        }
        
        try:
            print("🤖 Generating AI-powered lesson...")
            response = requests.post(f"{api_base}/generate-asl-lesson", json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                
                if result['success']:
                    print_lesson_preview(result['lesson_data'])
                    
                    # Show video info
                    video_data = result.get('video_data')
                    if video_data:
                        print(f"\n🎥 Video Generated:")
                        print(f"   File: {video_data['video_file']}")
                        print(f"   Duration: {video_data['duration']:.1f}s")
                        print(f"   Signs Used: {', '.join(video_data['signs'])}")
                    
                    # Show AI status
                    ai_status = "✅ AI Generated" if result['ai_available'] else "🔄 Fallback Rules"
                    print(f"\n🤖 Generation Method: {ai_status}")
                    print(f"💬 Message: {result['message']}")
                    
                else:
                    print(f"❌ Generation failed: {result['message']}")
            else:
                print(f"❌ API Error: {response.status_code}")
                print(f"Response: {response.text}")
                
        except requests.exceptions.Timeout:
            print("⏰ Request timed out")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("\n" + "-"*40)
        time.sleep(1)  # Brief pause between demos

def demo_ai_status():
    """Demo AI status checking"""
    print_section("AI STATUS CHECK")
    
    try:
        response = requests.get("http://127.0.0.1:8000/api/ai-status", timeout=5)
        
        if response.status_code == 200:
            status = response.json()
            print(f"🤖 AI Service: {status['service']}")
            print(f"✅ Available: {'Yes' if status['ai_available'] else 'No'}")
            print(f"💬 Status: {status['message']}")
            
            if status['ai_available']:
                print("\n🎉 AI is ready to generate optimized ASL lessons!")
            else:
                print("\n🔄 Using smart fallback rules (still very effective!)")
        
    except Exception as e:
        print(f"❌ Failed to check AI status: {e}")

def demo_preview_only():
    """Demo preview functionality (no video generation)"""
    print_section("PREVIEW-ONLY DEMO")
    
    payload = {
        "lesson_title": "Quick Science Preview",
        "lesson_text": "The sun gives light and heat. Plants need sunlight to grow."
    }
    
    try:
        print("🔍 Generating preview (no video)...")
        response = requests.post("http://127.0.0.1:8000/api/preview-lesson", json=payload, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            
            if result['success']:
                print_lesson_preview(result['lesson_data'])
                print(f"\n⚡ Preview generated in record time!")
                print(f"🤖 AI Available: {'Yes' if result['ai_available'] else 'No'}")
            else:
                print(f"❌ Preview failed: {result['message']}")
        else:
            print(f"❌ API Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Run complete demo"""
    print("🎓 ASL Classroom Platform - AI Lesson Generation Demo")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Check if servers are running
    try:
        health_response = requests.get("http://127.0.0.1:8000/api/health", timeout=3)
        if health_response.status_code != 200:
            print("❌ Backend server not responding. Please start it first:")
            print("   cd backend && python -m app.main")
            return
    except:
        print("❌ Backend server not responding. Please start it first:")
        print("   cd backend && python -m app.main")
        return
    
    try:
        frontend_response = requests.get("http://localhost:3000", timeout=3)
        if frontend_response.status_code != 200:
            print("⚠️ Frontend server may not be running. Start it with:")
            print("   cd frontend && npm run dev")
    except:
        print("⚠️ Frontend server may not be running. Start it with:")
        print("   cd frontend && npm run dev")
    
    print("\n🚀 Starting demo...\n")
    
    # Run demos
    demo_ai_status()
    demo_preview_only()
    demo_ai_lesson_generation()
    
    print_section("DEMO COMPLETE")
    print("🎉 AI Lesson Generation Demo Finished!")
    print("\n📚 Next Steps:")
    print("1. Open http://localhost:3000/create-lesson in your browser")
    print("2. Try creating your own AI-powered lessons")
    print("3. Add GEMINI_API_KEY to backend/.env for full AI features")
    print("4. Explore the enhanced UI with AI status indicators")

if __name__ == "__main__":
    main()
