#!/usr/bin/env python3
"""
Test the complete frontend flow by simulating what should happen
"""

import requests
import json

def test_complete_flow():
    """Test the complete AI lesson generation flow"""
    
    print("🧪 Testing Complete AI Lesson Flow...")
    
    # Step 1: Generate AI lesson with images
    print("\n1️⃣ Generating AI lesson...")
    response = requests.post(
        "http://127.0.0.1:8000/api/generate-asl-lesson",
        headers={"Content-Type": "application/json"},
        json={
            "lesson_title": "Frontend Test",
            "lesson_text": "Hello beautiful world",
            "use_ai": True
        },
        timeout=120
    )
    
    if response.status_code == 200:
        data = response.json()
        print("✅ API Response received!")
        print(f"   Success: {data.get('success')}")
        print(f"   AI Available: {data.get('ai_available')}")
        print(f"   Message: {data.get('message')}")
        
        # Check image data
        image_data = data.get('image_data')
        if image_data:
            print(f"   🖼️ Images: {image_data.get('total_images', 0)} images generated")
            for i, img in enumerate(image_data.get('images', [])):
                print(f"      Image {i+1}: {img.get('concept')} -> {img.get('image_file')}")
                
                # Test if image is accessible
                img_url = f"http://127.0.0.1:8000/storage/processed/images/{img.get('image_file')}"
                img_response = requests.head(img_url, timeout=10)
                print(f"      Accessible: {'✅' if img_response.status_code == 200 else '❌'} ({img_response.status_code})")
        else:
            print("   ❌ No image data in response")
            
        # Check lesson data
        lesson_data = data.get('lesson_data', {})
        print(f"   📚 Lesson: {lesson_data.get('lesson_title')}")
        print(f"   📝 Sentences: {len(lesson_data.get('sentences', []))}")
        
        # Simulate frontend state
        print("\n2️⃣ Simulating Frontend Navigation...")
        frontend_state = {
            'lessonMode': True,
            'lessonTitle': lesson_data.get('lesson_title'),
            'sentences': lesson_data.get('sentences', []),
            'imageData': image_data,
            'isAIGenerated': True,
            'aiAvailable': data.get('ai_available')
        }
        
        print("   Frontend state would be:")
        for key, value in frontend_state.items():
            print(f"      {key}: {type(value).__name__} = {value is not None}")
            
        print("\n3️⃣ Expected Frontend Behavior:")
        if image_data and image_data.get('images'):
            print("   🖼️ Should display AI images grid")
            print("   📝 Should show lesson content")
            print("   ✅ Should NOT show blank page")
        else:
            print("   ❌ Would fall back to video or show blank")
            
    else:
        print(f"❌ API Error: {response.status_code}")
        print(f"Response: {response.text}")

if __name__ == "__main__":
    test_complete_flow()
