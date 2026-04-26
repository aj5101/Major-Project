"""
AI Lesson Generation Service using Gemini API
Converts lesson text into ASL-friendly format with structured output
"""

import json
import re
from typing import Dict, List, Optional, Any
import os
import asyncio
import uuid
from dotenv import load_dotenv

load_dotenv()

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    print("⚠️ Google Generative AI not installed. Run: pip install google-genai")

try:
    from .working_image_service import working_image_service
    AI_IMAGE_AVAILABLE = True
except ImportError:
    AI_IMAGE_AVAILABLE = False
    print("⚠️ AI image service not available")

class AILessonService:
    """Service for AI-powered ASL lesson generation"""
    
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.model = None
        
        if GEMINI_AVAILABLE and self.api_key:
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel('gemini-2.5-flash')
                print("✅ Gemini AI initialized successfully")
            except Exception as e:
                print(f"❌ Failed to initialize Gemini AI: {e}")
                self.model = None
        else:
            if not GEMINI_AVAILABLE:
                print("⚠️ Google Generative AI SDK not available")
            elif not self.api_key:
                print("⚠️ GEMINI_API_KEY not found in environment variables")
    
    def is_available(self) -> bool:
        """Check if AI service is available"""
        return GEMINI_AVAILABLE and self.model is not None
    
    def generate_asl_lesson(self, lesson_text: str, lesson_title: str = "Untitled Lesson") -> Dict:
        """
        Generate ASL-friendly lesson using AI
        
        Args:
            lesson_text: Original lesson text
            lesson_title: Title of the lesson
            
        Returns:
            Dict with structured ASL lesson data
        """
        if not self.is_available():
            return self._fallback_generation(lesson_text, lesson_title)
        
        try:
            prompt = self._build_prompt(lesson_text, lesson_title)
            
            response = self.model.generate_content(prompt)
            result_text = response.text
            
            # Parse JSON response
            lesson_data = self._parse_ai_response(result_text, lesson_text, lesson_title)
            
            return lesson_data
            
        except Exception as e:
            print(f"❌ AI generation failed: {e}")
            return self._fallback_generation(lesson_text, lesson_title)
    
    def _build_prompt(self, lesson_text: str, lesson_title: str) -> str:
        """Build the AI prompt for ASL lesson generation"""
        return f"""
You are an expert ASL (American Sign Language) educator. Convert the following lesson into ASL-friendly format.

LESSON TITLE: {lesson_title}
LESSON TEXT: {lesson_text}

RULES:
1. Remove unnecessary grammar words (articles, helping verbs, etc.)
2. Use simple, concrete words that have clear ASL signs
3. Break into short sentences (3-5 words max)
4. Focus on concepts that can be expressed visually
5. Maintain the core meaning and educational value
6. Consider vocabulary that has common ASL signs

OUTPUT FORMAT:
Return ONLY valid JSON in this exact format:
{{
  "lesson_title": "{lesson_title}",
  "sentences": [
    {{
      "original": "original sentence here",
      "simplified": "simplified ASL-friendly sentence",
      "asl_sequence": ["word1", "word2", "word3"]
    }}
  ]
}}

EXAMPLE:
Input: "Water evaporates from the surface and forms clouds in the sky."
Output:
{{
  "lesson_title": "Water Cycle",
  "sentences": [
    {{
      "original": "Water evaporates from the surface",
      "simplified": "water evaporate surface",
      "asl_sequence": ["water", "evaporate", "surface"]
    }},
    {{
      "original": "and forms clouds in the sky",
      "simplified": "water form clouds sky",
      "asl_sequence": ["water", "form", "clouds", "sky"]
    }}
  ]
}}

COMMON ASL WORDS TO USE:
- water, sun, moon, earth, sky, cloud, rain, snow
- learn, teach, book, school, student, teacher
- help, give, take, make, do, go, come
- big, small, hot, cold, good, bad, happy, sad
- one, two, three, four, five, many, few
- what, where, when, why, how
- name, know, understand, see, hear

Process the lesson now and return ONLY the JSON:
"""

    def _parse_ai_response(self, response_text: str, original_text: str, lesson_title: str) -> Dict:
        """Parse AI response and ensure valid structure"""
        try:
            # Extract JSON from response
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                json_str = json_match.group()
                data = json.loads(json_str)
                
                # Validate structure
                if "lesson_title" in data and "sentences" in data:
                    # Ensure each sentence has required fields
                    for sentence in data["sentences"]:
                        if "original" not in sentence:
                            sentence["original"] = ""
                        if "simplified" not in sentence:
                            sentence["simplified"] = sentence["original"]
                        if "asl_sequence" not in sentence:
                            # Extract words from simplified text
                            words = re.findall(r'\b\w+\b', sentence["simplified"].lower())
                            sentence["asl_sequence"] = words[:5]  # Limit to 5 words
                    
                    return data
            
            # If parsing fails, return fallback
            return self._fallback_generation(original_text, lesson_title)
            
        except json.JSONDecodeError:
            print("❌ Failed to parse AI JSON response")
            return self._fallback_generation(original_text, lesson_title)
    
    def _fallback_generation(self, lesson_text: str, lesson_title: str) -> Dict:
        """Fallback rule-based generation when AI is unavailable"""
        print("🔄 Using fallback rule-based generation")
        
        # Simple rule-based processing
        sentences = re.split(r'[.!?]+', lesson_text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        processed_sentences = []
        
        for sentence in sentences[:5]:  # Limit to 5 sentences
            # Simplify sentence
            simplified = self._simplify_sentence(sentence)
            
            # Extract key words for ASL sequence
            words = re.findall(r'\b\w+\b', simplified.lower())
            asl_sequence = words[:4]  # Limit to 4 key words
            
            processed_sentences.append({
                "original": sentence,
                "simplified": simplified,
                "asl_sequence": asl_sequence
            })
        
        return {
            "lesson_title": lesson_title,
            "sentences": processed_sentences,
            "fallback_used": True
        }
    
    def _simplify_sentence(self, sentence: str) -> str:
        """Simple rule-based sentence simplification"""
        # Remove articles and common filler words
        filler_words = ['the', 'a', 'an', 'and', 'or', 'but', 'so', 'because', 'is', 'are', 'was', 'were']
        
        words = sentence.lower().split()
        simplified_words = [word for word in words if word not in filler_words]
        
        # Limit to 5 words
        simplified_words = simplified_words[:5]
        
        return ' '.join(simplified_words)
    
    async def generate_ai_image_lesson(self, lesson_text: str, lesson_title: str = "Untitled Lesson") -> Dict:
        """
        Generate ASL lesson with AI images using image generation service
        
        Args:
            lesson_text: Original lesson text
            lesson_title: Title of the lesson
            
        Returns:
            Dict with structured ASL lesson data and AI-generated images
        """
        # First generate the lesson structure
        lesson_data = self.generate_asl_lesson(lesson_text, lesson_title)
        
        # Generate images using AI if available
        if AI_IMAGE_AVAILABLE and working_image_service.is_available():
            try:
                print("🖼️ Generating AI images for lesson...")
                
                # Create a concise text for image generation
                simplified_text = " ".join([s.get("simplified", "") for s in lesson_data.get("sentences", [])])
                
                # Generate images (typically 3 images for a lesson)
                image_results = await working_image_service.generate_asl_images_from_text(
                    simplified_text, 
                    num_images=3
                )
                
                if image_results and len(image_results) > 0:
                    # Images are already saved by the working service
                    image_files = []
                    
                    for image_result in image_results:
                        image_files.append({
                            "image_file": image_result["image_file"],
                            "concept": image_result["concept"],
                            "image_number": image_result["image_number"],
                            "provider": image_result["provider"]
                        })
                    
                    if image_files:
                        # Add image data to lesson
                        lesson_data["image_data"] = {
                            "images": image_files,
                            "total_images": len(image_files),
                            "ai_generated": True,
                            "text": simplified_text
                        }
                        
                        # Mark that AI images were used
                        lesson_data["ai_images_used"] = True
                        
                        return lesson_data
                    else:
                        print("❌ No images were successfully downloaded")
                        
            except Exception as e:
                print(f"❌ AI image generation failed: {e}")
        
        # Fallback to existing system (no images)
        print("🔄 Using fallback (no images)")
        return lesson_data

# Global instance
ai_lesson_service = AILessonService()

def generate_ai_lesson(lesson_text: str, lesson_title: str = "Untitled Lesson") -> Dict:
    """Convenience function to generate AI lesson"""
    return ai_lesson_service.generate_asl_lesson(lesson_text, lesson_title)

def is_ai_available() -> bool:
    """Check if AI lesson generation is available"""
    return ai_lesson_service.is_available()
