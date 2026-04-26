"""
Test Frontend API Integration
"""

import requests

def test_frontend_api_integration():
    """Test the exact same request that the frontend would make"""
    
    print("🔧 Testing Frontend API Integration")
    print("=" * 50)
    
    # Test the exact same endpoint and payload
    url = "http://localhost:8000/api/generate-asl"
    headers = {"Content-Type": "application/json"}
    payload = {"text": "Hello students welcome to class"}
    
    try:
        print(f"Making POST request to: {url}")
        print(f"Payload: {payload}")
        
        response = requests.post(url, json=payload, headers=headers)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success! Response: {data}")
            
            # Test if the video file is accessible
            video_url = f"http://localhost:8000{data['video_url']}"
            print(f"Testing video access: {video_url}")
            
            video_response = requests.head(video_url)
            print(f"Video Status: {video_response.status_code}")
            
            if video_response.status_code == 200:
                size = video_response.headers.get('content-length', 'N/A')
                print(f"✅ Video accessible! Size: {size} bytes")
            else:
                print(f"❌ Video not accessible: {video_response.status_code}")
                
        else:
            print(f"❌ Error Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")

if __name__ == "__main__":
    test_frontend_api_integration()
