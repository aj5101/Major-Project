#!/usr/bin/env python3
"""
Simple test for AI image generation
"""

import requests
import os
import json
import base64
from dotenv import load_dotenv

load_dotenv('backend/.env')

def generate_simple_asl_image():
    """Generate a simple ASL image"""
    api_key = os.getenv("IMAGE_API_KEY")
    
    if not api_key:
        print("❌ No IMAGE_API_KEY found in .env")
        return
    
    print("🖼️ Testing Stable Diffusion API...")
    
    # Simple payload that should work
    payload = {
        "text_prompts": [
            {
                "text": "Clear ASL sign language hand gesture for hello, educational style, white background",
                "weight": 1.0
            }
        ],
        "width": 1024,
        "height": 1024,
        "samples": 1,
        "steps": 20,
        "cfg_scale": 7.0
    }
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    try:
        print("📤 Sending request to Stable Diffusion...")
        response = requests.post(
            "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image",
            headers=headers,
            json=payload,  # Use json parameter instead of data
            timeout=60
        )
        
        print(f"📥 Response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Image generation successful!")
            
            # Extract base64 image
            artifacts = result.get("artifacts", [])
            if artifacts and len(artifacts) > 0:
                base64_image = artifacts[0].get("base64")
                if base64_image:
                    # Save the image
                    image_data = base64.b64decode(base64_image)
                    with open("test_asl_hello.png", "wb") as f:
                        f.write(image_data)
                    print("💾 Image saved as: test_asl_hello.png")
                    return True
            
            print("❌ No image data in response")
            return False
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Error details: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

if __name__ == "__main__":
    success = generate_simple_asl_image()
    if success:
        print("\n🎉 Test completed successfully!")
        print("You can now open 'test_asl_hello.png' to see the generated ASL image.")
    else:
        print("\n❌ Test failed. Check the error messages above.")
