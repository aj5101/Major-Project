#!/usr/bin/env python3
"""
Test AI Lesson Generation Flow
Comprehensive test for the new AI-powered ASL lesson generation
"""

import sys
import os
import json
import requests
import time
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

def test_ai_service_import():
    """Test if AI lesson service can be imported"""
    print("🧪 Testing AI Service Import...")
    try:
        from backend.app.services.ai_lesson_service import generate_ai_lesson, is_ai_available
        print("✅ AI service imported successfully")
        
        # Check AI availability
        ai_available = is_ai_available()
        print(f"🤖 AI Available: {'Yes' if ai_available else 'No'}")
        
        return True, ai_available
    except ImportError as e:
        print(f"❌ Failed to import AI service: {e}")
        return False, False
    except Exception as e:
        print(f"❌ Error checking AI service: {e}")
        return False, False

def test_ai_lesson_generation():
    """Test AI lesson generation with sample text"""
    print("\n🧪 Testing AI Lesson Generation...")
    
    try:
        from backend.app.services.ai_lesson_service import generate_ai_lesson
        
        # Sample lesson text
        lesson_title = "Water Cycle"
        lesson_text = "Water evaporates from the surface when heated by the sun. The water vapor rises and forms clouds in the atmosphere. When the clouds become heavy, precipitation occurs and water returns to Earth."
        
        print(f"📝 Input: {lesson_title}")
        print(f"📄 Text: {lesson_text}")
        
        # Generate AI lesson
        result = generate_ai_lesson(lesson_text, lesson_title)
        
        print("✅ AI lesson generation completed")
        print(f"📊 Result structure: {list(result.keys())}")
        
        # Validate structure
        required_keys = ["lesson_title", "sentences"]
        for key in required_keys:
            if key not in result:
                print(f"❌ Missing required key: {key}")
                return False
        
        print(f"📖 Generated {len(result['sentences'])} sentences")
        
        # Display first sentence as example
        if result["sentences"]:
            first_sentence = result["sentences"][0]
            print(f"\n📌 Example Sentence:")
            print(f"   Original: {first_sentence.get('original', 'N/A')}")
            print(f"   Simplified: {first_sentence.get('simplified', 'N/A')}")
            print(f"   ASL Sequence: {first_sentence.get('asl_sequence', 'N/A')}")
        
        return True, result
        
    except Exception as e:
        print(f"❌ AI lesson generation failed: {e}")
        return False, None

def test_api_endpoint():
    """Test the API endpoint directly"""
    print("\n🧪 Testing API Endpoint...")
    
    # API base URL
    base_url = "http://127.0.0.1:8000/api"
    
    try:
        # Test health check
        print("🏥 Testing health endpoint...")
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Health check passed")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
        
        # Test AI status
        print("🤖 Testing AI status endpoint...")
        response = requests.get(f"{base_url}/ai-status", timeout=5)
        if response.status_code == 200:
            ai_status = response.json()
            print(f"✅ AI Status: {ai_status}")
        else:
            print(f"❌ AI status check failed: {response.status_code}")
            return False
        
        # Test lesson generation
        print("📚 Testing lesson generation endpoint...")
        lesson_data = {
            "lesson_title": "Test Water Cycle",
            "lesson_text": "Water evaporates and forms clouds.",
            "use_ai": True
        }
        
        response = requests.post(
            f"{base_url}/generate-asl-lesson",
            json=lesson_data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Lesson generation API successful")
            print(f"📊 Response keys: {list(result.keys())}")
            
            if result.get("success"):
                lesson_data = result.get("lesson_data", {})
                video_data = result.get("video_data", {})
                
                print(f"📖 Sentences: {len(lesson_data.get('sentences', []))}")
                print(f"🎥 Video generated: {'Yes' if video_data else 'No'}")
                
                return True
            else:
                print(f"❌ API returned failure: {result.get('message')}")
                return False
        else:
            print(f"❌ Lesson generation failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API server. Is the backend running?")
        return False
    except Exception as e:
        print(f"❌ API test failed: {e}")
        return False

def test_video_pipeline():
    """Test video generation pipeline"""
    print("\n🧪 Testing Video Pipeline...")
    
    try:
        from dynamic_asl_generator import create_video_for_text
        
        test_text = "water evaporate cloud"
        print(f"🎬 Testing video generation for: '{test_text}'")
        
        result = create_video_for_text(test_text)
        
        print("✅ Video generation successful")
        print(f"📁 Video file: {result['video_file']}")
        print(f"🎯 Signs used: {result['signs']}")
        print(f"⏱️ Duration: {result['duration']:.1f}s")
        
        return True, result
        
    except Exception as e:
        print(f"❌ Video pipeline test failed: {e}")
        return False, None

def test_complete_flow():
    """Test the complete AI lesson generation flow"""
    print("\n🧪 Testing Complete Flow...")
    
    try:
        # Import the AI lesson route function
        from backend.app.routes.ai_lesson import LessonRequest
        from backend.app.services.ai_lesson_service import generate_ai_lesson
        from dynamic_asl_generator import create_video_for_text
        
        # Sample lesson
        lesson_title = "Simple Science"
        lesson_text = "The sun gives light. Plants need sunlight. Water helps plants grow."
        
        print(f"📚 Lesson: {lesson_title}")
        print(f"📄 Content: {lesson_text}")
        
        # Step 1: Generate AI lesson
        print("\n1️⃣ Generating AI lesson...")
        ai_result = generate_ai_lesson(lesson_text, lesson_title)
        
        if not ai_result or "sentences" not in ai_result:
            print("❌ AI lesson generation failed")
            return False
        
        print(f"✅ Generated {len(ai_result['sentences'])} AI-processed sentences")
        
        # Step 2: Extract ASL sequences
        print("\n2️⃣ Extracting ASL sequences...")
        all_asl_words = []
        for sentence in ai_result["sentences"]:
            asl_sequence = sentence.get("asl_sequence", [])
            all_asl_words.extend(asl_sequence)
            print(f"   '{sentence['original']}' → '{sentence['simplified']}' → {asl_sequence}")
        
        # Step 3: Generate video
        print("\n3️⃣ Generating ASL video...")
        video_text = " ".join(all_asl_words) if all_asl_words else lesson_text
        video_result = create_video_for_text(video_text)
        
        print(f"✅ Video generated: {video_result['video_file']}")
        print(f"🎯 Signs: {video_result['signs']}")
        print(f"⏱️ Duration: {video_result['duration']:.1f}s")
        
        # Step 4: Create final package
        print("\n4️⃣ Creating final lesson package...")
        final_package = {
            "lesson_title": ai_result["lesson_title"],
            "sentences": ai_result["sentences"],
            "video_data": video_result,
            "ai_generated": True,
            "total_duration": video_result["duration"]
        }
        
        print("✅ Complete flow successful!")
        print(f"📦 Package contains {len(final_package['sentences'])} sentences and video")
        
        return True, final_package
        
    except Exception as e:
        print(f"❌ Complete flow test failed: {e}")
        return False, None

def main():
    """Run all tests"""
    print("🚀 Starting AI Lesson Generation Flow Tests")
    print("=" * 50)
    
    results = {}
    
    # Test 1: AI Service Import
    success, ai_available = test_ai_service_import()
    results["ai_import"] = success
    results["ai_available"] = ai_available
    
    # Test 2: AI Lesson Generation
    if success:
        success, ai_result = test_ai_lesson_generation()
        results["ai_generation"] = success
        results["ai_result"] = ai_result
    
    # Test 3: Video Pipeline
    success, video_result = test_video_pipeline()
    results["video_pipeline"] = success
    results["video_result"] = video_result
    
    # Test 4: API Endpoint (optional - requires server running)
    try:
        api_success = test_api_endpoint()
        results["api_endpoint"] = api_success
    except:
        results["api_endpoint"] = None
        print("\n⚠️ API test skipped (server not running)")
    
    # Test 5: Complete Flow
    if results.get("ai_generation") and results.get("video_pipeline"):
        success, final_package = test_complete_flow()
        results["complete_flow"] = success
        results["final_package"] = final_package
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
    for test_name, result in results.items():
        if isinstance(result, bool):
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{test_name:20} → {status}")
        elif isinstance(result, dict) or result is None:
            continue  # Skip detailed results
    
    # Overall status
    critical_tests = ["ai_import", "ai_generation", "video_pipeline", "complete_flow"]
    all_passed = all(results.get(test, False) for test in critical_tests)
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 ALL CRITICAL TESTS PASSED!")
        print("🚀 AI Lesson Generation is ready to use!")
    else:
        print("⚠️ Some tests failed. Check the details above.")
    
    print("=" * 50)

if __name__ == "__main__":
    main()
