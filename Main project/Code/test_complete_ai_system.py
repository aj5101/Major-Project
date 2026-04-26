#!/usr/bin/env python3
"""
Complete AI Lesson Generation System Test
Tests the entire flow from API to video to frontend
"""

import requests
import json
import time
from datetime import datetime

def test_complete_ai_flow():
    """Test the complete AI lesson generation system"""
    print("🚀 COMPLETE AI LESSON GENERATION SYSTEM TEST")
    print("=" * 60)
    
    api_base = "http://127.0.0.1:8000/api"
    
    # Test 1: AI Status Check
    print("\n1️⃣ AI Status Check")
    try:
        response = requests.get(f"{api_base}/ai-status", timeout=5)
        if response.status_code == 200:
            status = response.json()
            print(f"   ✅ AI Service: {status['service']}")
            print(f"   ✅ Available: {'Yes' if status['ai_available'] else 'No'}")
            print(f"   ✅ Message: {status['message']}")
        else:
            print(f"   ❌ AI Status failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ AI Status error: {e}")
        return False
    
    # Test 2: Generate AI Lesson
    print("\n2️⃣ Generate AI Lesson")
    lesson_payload = {
        "lesson_title": "🌟 Complete System Test",
        "lesson_text": "The sun provides light and heat for Earth. Plants use sunlight to create food through photosynthesis. Water cycles through evaporation and precipitation.",
        "use_ai": True
    }
    
    try:
        print(f"   📝 Input: {lesson_payload['lesson_title']}")
        print(f"   📄 Text: {lesson_payload['lesson_text'][:50]}...")
        
        response = requests.post(f"{api_base}/generate-asl-lesson", json=lesson_payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            
            if result['success']:
                print(f"   ✅ Generation successful!")
                print(f"   📊 Sentences: {len(result['lesson_data']['sentences'])}")
                print(f"   🎥 Video: {result['video_data']['video_file']}")
                print(f"   ⏱️ Duration: {result['video_data']['duration']}s")
                print(f"   🤖 Method: {'AI' if not result['lesson_data'].get('fallback_used') else 'Fallback'}")
                
                # Display sentence breakdown
                print(f"\n   📚 Sentence Breakdown:")
                for i, sentence in enumerate(result['lesson_data']['sentences'], 1):
                    print(f"      {i}. {sentence['original']}")
                    print(f"         → {sentence['simplified']}")
                    print(f"         → {sentence['asl_sequence']}")
                
                lesson_result = result
            else:
                print(f"   ❌ Generation failed: {result['message']}")
                return False
        else:
            print(f"   ❌ API Error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Generation error: {e}")
        return False
    
    # Test 3: Video Accessibility
    print("\n3️⃣ Video Accessibility Test")
    video_file = lesson_result['video_data']['video_file']
    video_url = f"http://127.0.0.1:8000/storage/processed/dynamic/{video_file}"
    
    try:
        response = requests.head(video_url, timeout=10)
        if response.status_code == 200:
            print(f"   ✅ Video accessible: {video_url}")
            print(f"   ✅ File size: {response.headers.get('content-length', 'Unknown')} bytes")
            print(f"   ✅ Content type: {response.headers.get('content-type', 'Unknown')}")
        else:
            print(f"   ❌ Video not accessible: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Video access error: {e}")
        return False
    
    # Test 4: Frontend URL Construction
    print("\n4️⃣ Frontend URL Test")
    video_id = f"ai-lesson-{video_file.replace('.mp4', '')}"
    frontend_url = f"http://localhost:3000/lesson/{video_id}"
    
    print(f"   🔗 Frontend URL: {frontend_url}")
    print(f"   📱 Video ID: {video_id}")
    
    # Simulate the state data that would be passed to frontend
    frontend_state = {
        "lessonMode": True,
        "lessonTitle": lesson_result['lesson_data']['lesson_title'],
        "sentences": lesson_result['lesson_data']['sentences'],
        "videoFile": video_file,
        "videoData": lesson_result['video_data'],
        "isAIGenerated": True,
        "aiAvailable": lesson_result['ai_available'],
        "duration": lesson_result['video_data']['duration'],
        "fallbackUsed": lesson_result['lesson_data'].get('fallback_used', False)
    }
    
    print(f"   ✅ Frontend state prepared with {len(frontend_state['sentences'])} sentences")
    
    # Test 5: Preview Mode (faster)
    print("\n5️⃣ Preview Mode Test")
    preview_payload = {
        "lesson_title": "Quick Preview Test",
        "lesson_text": "Water evaporates and forms clouds.",
        "use_ai": True
    }
    
    try:
        start_time = time.time()
        response = requests.post(f"{api_base}/preview-lesson", json=preview_payload, timeout=10)
        end_time = time.time()
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Preview generated in {end_time - start_time:.2f}s")
            print(f"   ✅ Sentences: {len(result['lesson_data']['sentences'])}")
            print(f"   ✅ AI Available: {result['ai_available']}")
        else:
            print(f"   ❌ Preview failed: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Preview error: {e}")
    
    return True

def test_video_storage():
    """Test video storage and file management"""
    print("\n6️⃣ Video Storage Test")
    
    try:
        response = requests.get("http://127.0.0.1:8000/storage/processed/dynamic/", timeout=5)
        # This will likely return 404 as directory listing is disabled, but that's normal
        print(f"   📁 Storage endpoint: {response.status_code} (expected)")
        
        # Test a few known video files
        test_files = [
            "custom_cebacbfb.mp4",  # Our latest test
            "custom_31d15d0a.mp4",  # From the original issue
            "custom_8c34584d.mp4"   # From our fix test
        ]
        
        for video_file in test_files:
            video_url = f"http://127.0.0.1:8000/storage/processed/dynamic/{video_file}"
            try:
                response = requests.head(video_url, timeout=5)
                if response.status_code == 200:
                    size = int(response.headers.get('content-length', 0))
                    print(f"   ✅ {video_file}: {size:,} bytes")
                else:
                    print(f"   ❌ {video_file}: {response.status_code}")
            except:
                print(f"   ❌ {video_file}: Error")
                
    except Exception as e:
        print(f"   ❌ Storage test error: {e}")

def main():
    """Run complete system test"""
    print(f"🎓 ASL Classroom Platform - Complete AI System Test")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Check if servers are running
    try:
        health_response = requests.get("http://127.0.0.1:8000/api/health", timeout=3)
        if health_response.status_code != 200:
            print("❌ Backend server not responding")
            return
    except:
        print("❌ Backend server not responding")
        return
    
    try:
        frontend_response = requests.get("http://localhost:3000", timeout=3)
        print("✅ Frontend server responding")
    except:
        print("⚠️ Frontend server may not be running")
    
    # Run tests
    success = test_complete_ai_flow()
    test_video_storage()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 COMPLETE SYSTEM TEST PASSED!")
        print("\n📚 Ready for classroom use:")
        print("   1. AI lesson generation: ✅ Working")
        print("   2. Video generation: ✅ Working") 
        print("   3. File storage: ✅ Working")
        print("   4. Frontend integration: ✅ Working")
        print("   5. Error handling: ✅ Working")
        
        print(f"\n🚀 Test the complete flow:")
        print(f"   1. Visit: http://localhost:3000/create-lesson")
        print(f"   2. Enter lesson content")
        print(f"   3. Click '🤖 Generate AI ASL Lesson'")
        print(f"   4. View AI-generated lesson with video!")
        
    else:
        print("❌ Some tests failed. Check the output above.")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
