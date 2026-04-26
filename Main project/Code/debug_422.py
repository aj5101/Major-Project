"""
Debug 422 Error
"""

import requests
import json

def debug_422_error():
    """Debug the 422 validation error"""
    
    print("🔧 Debugging 422 Error")
    print("=" * 50)
    
    # Test different request formats
    test_cases = [
        {"text": "Hello students welcome to class"},
        {"text": "Hello students welcome to class", "video_id": None},
        {"text": "Hello students welcome to class", "video_id": "test123"},
        {"text": "Hello students welcome to class", "video_id": ""}
    ]
    
    url = "http://localhost:8000/api/generate-asl"
    headers = {"Content-Type": "application/json"}
    
    for i, payload in enumerate(test_cases):
        print(f"\nTest {i+1}: {payload}")
        
        try:
            response = requests.post(url, json=payload, headers=headers)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Success: {data['video_file']}")
            elif response.status_code == 422:
                print(f"   ❌ 422 Error: {response.text}")
                # Try to parse the error
                try:
                    error_data = response.json()
                    print(f"   Error Details: {error_data}")
                except:
                    pass
            else:
                print(f"   ❌ Other Error: {response.text}")
                
        except Exception as e:
            print(f"   ❌ Exception: {e}")
    
    # Test the exact format the frontend should send
    print(f"\n" + "=" * 50)
    print("🔍 Expected Request Format:")
    print("   POST /api/generate-asl")
    print("   Content-Type: application/json")
    print("   Body: {\"text\": \"your text here\"}")
    
    print(f"\n📋 Common 422 Causes:")
    print("   1. Missing required field 'text'")
    print("   2. Invalid data types")
    print("   3. Extra fields not allowed")
    print("   4. Empty or null values")

if __name__ == "__main__":
    debug_422_error()
