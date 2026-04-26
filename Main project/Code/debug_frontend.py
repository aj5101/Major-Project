"""
Debug Frontend Issues
"""

def debug_frontend_issues():
    """Check common frontend issues"""
    
    print("🔧 Debugging Frontend Issues")
    print("=" * 50)
    
    # Test 1: Check API endpoints
    print("\n1. Testing API endpoints...")
    import requests
    
    endpoints = [
        ("Health", "GET", "http://localhost:8000/api/health"),
        ("Available Signs", "GET", "http://localhost:8000/api/available-signs"),
        ("Generate ASL", "POST", "http://localhost:8000/api/generate-asl")
    ]
    
    for name, method, url in endpoints:
        try:
            if method == "GET":
                response = requests.get(url)
            else:
                response = requests.post(url, json={"text": "Hello students"})
            
            print(f"   {name}: {response.status_code} {'✅' if response.status_code == 200 else '❌'}")
            
            if response.status_code != 200:
                print(f"     Error: {response.text}")
                
        except Exception as e:
            print(f"   {name}: ❌ {e}")
    
    # Test 2: Check video files
    print("\n2. Testing video file access...")
    test_videos = [
        "http://localhost:8000/storage/processed/dynamic/custom_689b0e46.mp4",
        "http://localhost:8000/storage/processed/preset_videos/phrase_01.mp4"
    ]
    
    for video_url in test_videos:
        try:
            response = requests.head(video_url)
            print(f"   {video_url.split('/')[-1]}: {response.status_code} {'✅' if response.status_code == 200 else '❌'}")
        except Exception as e:
            print(f"   {video_url.split('/')[-1]}: ❌ {e}")
    
    # Test 3: Check CORS
    print("\n3. Testing CORS...")
    try:
        response = requests.options("http://localhost:8000/api/generate-asl")
        cors_headers = {
            'access-control-allow-origin': response.headers.get('access-control-allow-origin'),
            'access-control-allow-methods': response.headers.get('access-control-allow-methods'),
            'access-control-allow-headers': response.headers.get('access-control-allow-headers')
        }
        print(f"   CORS Headers: {cors_headers}")
    except Exception as e:
        print(f"   CORS Test: ❌ {e}")
    
    print("\n" + "=" * 50)
    print("🔍 Common Frontend Issues to Check:")
    print("   1. Browser Console Errors (F12 → Console)")
    print("   2. Network Tab Errors (F12 → Network)")
    print("   3. JavaScript Errors in Console")
    print("   4. CORS Issues")
    print("   5. API Response Format Issues")
    
    print("\n📋 What to Check in Browser:")
    print("   • Open Developer Tools (F12)")
    print("   • Look at Console tab for JavaScript errors")
    print("   • Look at Network tab for failed requests")
    print("   • Check the exact error message")

if __name__ == "__main__":
    debug_frontend_issues()
