"""
Working AI Image Generation Service
Uses the exact code that works in our test
"""

import os
import requests
import json
import base64
import uuid
import urllib3
from typing import Optional, Dict, Any, List
from dotenv import load_dotenv

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

load_dotenv()

class WorkingImageService:
    """Service that we know works for AI image generation"""
    
    def __init__(self):
        self.api_key = os.getenv("IMAGE_API_KEY")
        
    def is_available(self) -> bool:
        return bool(self.api_key)
    
    async def generate_asl_images_from_text(self, text: str, num_images: int = 3) -> Optional[List[Dict[str, Any]]]:
        """Generate ASL images using the working approach"""
        if not self.is_available():
            print("⚠️ AI image API key not found")
            return None
        
        try:
            print(f"🖼️ Generating {num_images} ASL images for: '{text}'")
            
            # Split text into concepts
            words = text.split()
            if len(words) > num_images:
                words = words[:num_images]
            elif len(words) < num_images:
                words = words + [words[-1]] * (num_images - len(words))
            
            images = []
            
            for i, concept in enumerate(words[:num_images]):
                image_result = await self._generate_single_image(concept, i+1)
                if image_result:
                    images.append(image_result)
                    print(f"✅ Generated image {i+1}: {concept}")
                else:
                    print(f"❌ Failed to generate image for: '{concept}'")
            
            return images if images else None
            
        except Exception as e:
            print(f"❌ Error generating ASL images: {e}")
            return None
    
    async def _generate_single_image(self, concept: str, image_num: int) -> Optional[Dict[str, Any]]:
        """Generate a single ASL image"""
        try:
            # Use the exact working payload from our test
            payload = {
                "text_prompts": [
                    {
                        "text": f"Clear ASL sign language hand gesture for {concept}, educational style, white background, high quality",
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
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
            
            response = requests.post(
                "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image",
                headers=headers,
                json=payload,
                timeout=60,
                verify=False
            )
            
            if response.status_code == 200:
                result = response.json()
                artifacts = result.get("artifacts", [])
                if artifacts and len(artifacts) > 0:
                    base64_image = artifacts[0].get("base64")
                    if base64_image:
                        # Save image to local storage
                        _svc_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
                        storage_path = os.getenv("STORAGE_PATH", os.path.join(_svc_root, "storage"))
                        image_dir = os.path.join(storage_path, "processed", "images")
                        os.makedirs(image_dir, exist_ok=True)
                        
                        image_filename = f"asl_image_{uuid.uuid4().hex[:8]}_{image_num}.png"
                        local_path = os.path.join(image_dir, image_filename)
                        
                        # Decode and save
                        image_data = base64.b64decode(base64_image)
                        with open(local_path, "wb") as f:
                            f.write(image_data)
                        
                        print(f"💾 Image saved: {image_filename}")
                        
                        return {
                            "image_file": image_filename,
                            "concept": concept,
                            "image_number": image_num,
                            "provider": "stable-diffusion"
                        }
            
            print(f"❌ API Error ({response.status_code}): {response.text[:200]}")
            return None
            
        except Exception as e:
            print(f"❌ Error generating image for '{concept}': {e}")
            return None

# Global instance
working_image_service = WorkingImageService()
