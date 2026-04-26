"""
AI Image Generation Service
Uses AI image generation to create ASL images from text
"""

import os
import requests
import json
import time
import uuid
from typing import Optional, Dict, Any, List

class AIImageService:
    """Service for AI-powered ASL image generation"""
    
    def __init__(self):
        self.image_api_key = os.getenv("IMAGE_API_KEY")
        self.image_api_provider = os.getenv("IMAGE_API_PROVIDER", "stable-diffusion")  # default provider
        self.base_url = self._get_base_url()
        
    def _get_base_url(self) -> str:
        """Get base URL based on provider"""
        if self.image_api_provider == "stable-diffusion":
            return "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0"
        elif self.image_api_provider == "openai-dalle":
            return "https://api.openai.com/v1"
        elif self.image_api_provider == "replicate":
            return "https://api.replicate.com/v1"
        else:
            return "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0"  # default
        
    def is_available(self) -> bool:
        """Check if AI image service is available"""
        return bool(self.image_api_key)
    
    async def generate_asl_images_from_text(self, text: str, num_images: int = 3) -> Optional[List[Dict[str, Any]]]:
        """
        Generate ASL images from text using AI image generation
        
        Args:
            text: The text to convert to ASL images
            num_images: Number of images to generate
            
        Returns:
            List of Dict with image information or None if failed
        """
        if not self.is_available():
            print("⚠️ AI image API key not found")
            return None
        
        try:
            print(f"🖼️ Generating {num_images} ASL images for: '{text}'")
            
            # Split text into individual words/concepts for image generation
            words = text.split()
            if len(words) > num_images:
                # Group words if too many
                words = [ " ".join(words[i:i+2]) for i in range(0, len(words), max(2, len(words)//num_images)) ]
                words = words[:num_images]
            elif len(words) < num_images:
                # Repeat words if too few
                words = words + [words[-1]] * (num_images - len(words))
            
            images = []
            
            for i, word in enumerate(words[:num_images]):
                # Generate ASL image for each word/concept
                image_result = await self._generate_single_asl_image(word, i+1)
                if image_result:
                    images.append(image_result)
                else:
                    print(f"❌ Failed to generate image for: '{word}'")
            
            if images:
                print(f"✅ Generated {len(images)} ASL images successfully!")
                return images
            else:
                print("❌ No images were generated")
                return None
                
        except Exception as e:
            print(f"❌ Error generating ASL images: {e}")
            return None
    
    async def _generate_single_asl_image(self, concept: str, image_num: int) -> Optional[Dict[str, Any]]:
        """Generate a single ASL image for a concept"""
        try:
            if self.image_api_provider == "stable-diffusion":
                return await self._generate_with_stable_diffusion(concept, image_num)
            elif self.image_api_provider == "openai-dalle":
                return await self._generate_with_dalle(concept, image_num)
            elif self.image_api_provider == "replicate":
                return await self._generate_with_replicate(concept, image_num)
            else:
                return await self._generate_with_stable_diffusion(concept, image_num)
                
        except Exception as e:
            print(f"❌ Error generating image for '{concept}': {e}")
            return None
    
    async def _generate_with_stable_diffusion(self, concept: str, image_num: int) -> Optional[Dict[str, Any]]:
        """Generate ASL image using Stable Diffusion"""
        headers = {
            "Authorization": f"Bearer {self.image_api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "text_prompts": [
                {
                    "text": f"Clear ASL sign language hand gesture for '{concept}'. Educational style, white background, high quality, professional lighting, focused on hands and arms",
                    "weight": 1
                },
                {
                    "text": "blurry, low quality, distorted hands, unclear gestures, distracting background, text, watermark",
                    "weight": -1
                }
            ],
            "width": 1024,
            "height": 1024,
            "samples": 1,
            "steps": 25,
            "cfg_scale": 7.5,
            "seed": str(uuid.uuid4())[:8]
        }
        
        response = requests.post(
            f"{self.base_url}/text-to-image",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            image_url = result.get("artifacts", [])[0].get("base64") if result.get("artifacts") else None
            
            if image_url:
                return {
                    "image_url": f"data:image/png;base64,{image_url}",
                    "concept": concept,
                    "image_number": image_num,
                    "provider": "stable-diffusion"
                }
        else:
            print(f"❌ Stable Diffusion API Error ({response.status_code}): {response.text[:300]}")
        
        return None
    
    async def _generate_with_dalle(self, concept: str, image_num: int) -> Optional[Dict[str, Any]]:
        """Generate ASL image using DALL-E"""
        headers = {
            "Authorization": f"Bearer {self.image_api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "dall-e-3",
            "prompt": f"Clear ASL sign language hand gesture showing '{concept}'. Educational style, simple white background, professional quality, focused on clear hand positioning",
            "size": "512x512",
            "quality": "standard",
            "n": 1
        }
        
        response = requests.post(
            f"{self.base_url}/images/generations",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            image_url = result.get("data", [])[0].get("url") if result.get("data") else None
            
            if image_url:
                return {
                    "image_url": image_url,
                    "concept": concept,
                    "image_number": image_num,
                    "provider": "dall-e"
                }
        
        return None
    
    async def _generate_with_replicate(self, concept: str, image_num: int) -> Optional[Dict[str, Any]]:
        """Generate ASL image using Replicate"""
        headers = {
            "Authorization": f"Token {self.image_api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "version": "ac732df83cea7fff18b8472768c88ad041fa750ff7682a21affe81863cbe77e4",  # Stable Diffusion
            "input": {
                "prompt": f"Clear ASL sign language hand gesture for '{concept}'. Educational style, white background, high quality, professional lighting",
                "negative_prompt": "blurry, low quality, distorted hands, unclear gestures, distracting background",
                "width": 512,
                "height": 512,
                "num_outputs": 1,
                "num_inference_steps": 25,
                "guidance_scale": 7.5
            }
        }
        
        response = requests.post(
            f"{self.base_url}/predictions",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            # For Replicate, we'd need to poll for completion
            # Simplified for now
            image_url = result.get("output", [])
            
            if image_url:
                return {
                    "image_url": image_url[0] if isinstance(image_url, list) else image_url,
                    "concept": concept,
                    "image_number": image_num,
                    "provider": "replicate"
                }
        
        return None
    
    async def download_image(self, image_url: str, local_path: str) -> bool:
        """
        Download image from URL to local storage
        
        Args:
            image_url: URL of the generated image
            local_path: Local path to save the image
            
        Returns:
            True if successful, False otherwise
        """
        try:
            print(f"📥 Downloading image from: {image_url}")
            
            # Handle base64 images
            if image_url.startswith("data:image/"):
                import base64
                header, data = image_url.split(",", 1)
                image_data = base64.b64decode(data)
                
                # Ensure directory exists
                os.makedirs(os.path.dirname(local_path), exist_ok=True)
                
                with open(local_path, 'wb') as f:
                    f.write(image_data)
            else:
                # Handle URL images
                response = requests.get(image_url, stream=True, timeout=30)
                response.raise_for_status()
                
                # Ensure directory exists
                os.makedirs(os.path.dirname(local_path), exist_ok=True)
                
                with open(local_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
            
            print(f"✅ Image downloaded to: {local_path}")
            return True
            
        except Exception as e:
            print(f"❌ Error downloading image: {e}")
            return False

# Global instance
ai_image_service = AIImageService()
