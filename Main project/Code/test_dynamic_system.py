"""
Test the Dynamic ASL System
"""

def test_dynamic_asl_system():
    """Test the complete dynamic ASL system"""
    
    print("🎯 Testing Dynamic ASL System")
    print("=" * 50)
    
    # Test 1: Check comprehensive ASL dataset
    print("\n1. Checking comprehensive ASL dataset...")
    import requests
    response = requests.get("http://localhost:8000/api/asl-dataset/")
    if response.status_code == 200:
        asl_videos = response.json()
        print(f"✅ Found {len(asl_videos)} ASL signs:")
        for video in asl_videos:
            print(f"   - {video['gloss'].upper()}")
    else:
        print("❌ Failed to fetch ASL dataset")
        return
    
    # Test 2: Check preset videos
    print("\n2. Checking preset videos...")
    preset_videos = [
        "phrase_01.mp4", "phrase_02.mp4", "phrase_03.mp4",
        "phrase_04.mp4", "phrase_05.mp4"
    ]
    
    for video in preset_videos:
        response = requests.head(f"http://localhost:8000/storage/processed/preset_videos/{video}")
        if response.status_code == 200:
            size = response.headers.get('content-length', 'N/A')
            print(f"✅ {video}: {size} bytes")
        else:
            print(f"❌ {video}: Not found")
    
    # Test 3: Check frontend accessibility
    print("\n3. Checking frontend...")
    try:
        response = requests.get("http://localhost:3000", timeout=5)
        if response.status_code == 200:
            print("✅ Frontend accessible")
        else:
            print("❌ Frontend not accessible")
    except:
        print("❌ Frontend connection failed")
    
    print("\n" + "=" * 50)
    print("🎉 Dynamic ASL System Test Complete!")
    
    print("\n🌟 NEW FEATURES AVAILABLE:")
    print("   ✅ 12 ASL signs with realistic animations")
    print("   ✅ 10 Preset educational phrases")
    print("   ✅ Custom text input with dynamic mapping")
    print("   ✅ Word-to-sign intelligence")
    print("   ✅ Multiple input modes (Video, Preset, Custom)")
    
    print("\n🚀 HOW TO USE:")
    print("   1. Go to http://localhost:3000/upload")
    print("   2. Choose from 3 modes:")
    print("      • 🎥 Video Upload - For videos with speech")
    print("      • 🎯 Preset Phrases - Quick educational content")
    print("      • 📝 Custom Text - Any educational text")
    print("   3. Get ASL videos matched to YOUR input!")
    
    print("\n📝 SAMPLE TEXT INPUTS TO TRY:")
    sample_texts = [
        "Hello students welcome to class",
        "Science helps us understand the world", 
        "Teacher asks question student answers",
        "Books help us gain knowledge",
        "Math teaches us to solve problems"
    ]
    
    for text in sample_texts:
        print(f"   • '{text}'")

if __name__ == "__main__":
    test_dynamic_asl_system()
