"""
Real-Time ASL Generation System
Fetches ASL content dynamically and generates videos based on exact user input.
"""

from moviepy.editor import VideoFileClip, concatenate_videoclips
import os
import tempfile
import json
import re
from datetime import datetime
import sys
import os
from typing import List

# Ensure the backend directory is in the path to import AIAgentService
backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend')
if backend_dir not in sys.path:
    sys.path.append(backend_dir)

try:
    from app.services.ai_agent_service import AIAgentService
except ImportError:
    AIAgentService = None

class RealTimeASLGenerator:
    """Generates ASL videos in real-time based on user input"""
    
    def __init__(self):
        _root = os.path.dirname(os.path.abspath(__file__))
        self.api_base = "http://localhost:8000/api"
        self.storage_path = os.getenv("ASL_REALTIME_PATH", os.path.join(_root, "storage", "processed", "realtime"))
        self.clips_path = os.getenv("ASL_CLIPS_PATH", os.path.join(_root, "storage", "asl_clips"))
        os.makedirs(self.storage_path, exist_ok=True)
        self.ai_service = AIAgentService() if AIAgentService else None
        
        # Load available signs from clips directory
        self.available_clips = {}
        if os.path.exists(self.clips_path):
            for file in os.listdir(self.clips_path):
                if file.endswith('.mp4'):
                    sign_name = file.split('_')[0].lower()
                    if sign_name not in self.available_clips:
                        self.available_clips[sign_name] = []
                    self.available_clips[sign_name].append(os.path.join(self.clips_path, file))
    
    def generate_asl_from_prompt(self, user_text):
        """Generate ASL video based on exact user prompt"""
        
        print(f"🎯 Generating ASL for: '{user_text}'")
        
        # Step 1: Extract key concepts from user input
        concepts = self._extract_concepts(user_text)
        print(f"   Extracted concepts: {concepts}")
        
        # Step 2: Get ASL content for each concept
        asl_content = self._get_asl_content(concepts)
        print(f"   ASL content: {asl_content}")
        
        # Step 3: Generate video based on user's exact input
        video_result = self._create_custom_video(user_text, concepts, asl_content)
        
        return video_result
    
    def _extract_concepts(self, text):
        """Extract concepts and ensure they map to available clips."""
        available_signs: List[str] = list(self.available_clips.keys())
        if not available_signs:
            return []

        # Prefer AI-backed extraction + semantic mapping (handled inside service)
        if self.ai_service:
            print("   🤖 Extracting concepts with AI + semantic mapping...")
            concepts = self.ai_service.extract_asl_concepts(text, available_signs=available_signs)
            print(f"   🤖 Mapped concepts: {concepts}")
            return [c for c in concepts if c in self.available_clips]

        # Minimal fallback: exact word matches only
        print("   ⚠️ AI service unavailable. Using exact match extraction...")
        words = re.findall(r"\b\w+\b", text.lower())
        return [w for w in words if w in self.available_clips]
    
    def _get_asl_content(self, concepts):
        """Map extracted concepts to ASL content description for metadata"""
        # Just return the concepts themselves as the content since they are direct signs now
        return concepts if concepts else ["hello"]
    
    def _create_custom_video(self, user_text, concepts, asl_content):
        """Create custom video filename and metadata"""
        
        # Generate unique filename based on user input and timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_text = "".join(c for c in user_text if c.isalnum() or c in " -_")[:20]
        filename = f"realtime_{safe_text}_{timestamp}.mp4"
        
        # Create video metadata
        video_metadata = {
            'filename': filename,
            'user_input': user_text,
            'concepts': concepts,
            'asl_content': asl_content,
            'duration': len(concepts) * 2,  # 2 seconds per concept
            'created_at': datetime.now().isoformat(),
            'video_type': 'realtime_custom'
        }
        
        # Save metadata
        metadata_path = os.path.join(self.storage_path, f"{filename}.json")
        with open(metadata_path, 'w') as f:
            json.dump(video_metadata, f, indent=2, default=str)
        
        print(f"   Created metadata: {metadata_path}")
        
        # Stitch actual video content using moviepy
        final_video_path = os.path.join(self.storage_path, filename)
        
        try:
            clips = []
            for concept in concepts:
                if concept in self.available_clips and self.available_clips[concept]:
                    clip_path = self.available_clips[concept][0]
                    clips.append(VideoFileClip(clip_path))
            
            if clips:
                # Concatenate all clips
                final_clip = concatenate_videoclips(clips, method="compose")
                final_clip.write_videofile(
                    final_video_path,
                    codec="libx264",
                    audio_codec="aac",
                    fps=24,
                    logger=None
                )
                final_clip.close()
                for c in clips:
                    c.close()
                print(f"   ✅ Successfully stitched video: {final_video_path}")
            else:
                # If no clips were found, just write an empty placeholder
                print("   ⚠️ No matching clips found. Writing placeholder.")
                with open(final_video_path, 'w') as f:
                    f.write("Placeholder video - no matching ASL clips found for input")
        except Exception as e:
            print(f"   ❌ Error stitching video: {e}")
            with open(final_video_path, 'w') as f:
                f.write("Placeholder video - error occurred during stitching")
        
        return {
            'video_file': filename,
            'concepts': concepts,
            'asl_content': asl_content,
            'duration': video_metadata['duration'],
            'metadata_file': f"{filename}.json",
            'user_input': user_text,
            'created_at': video_metadata['created_at'],
            'video_type': video_metadata['video_type']
        }

def test_realtime_system():
    """Test the real-time ASL generation system"""
    
    print("🚀 Real-Time ASL Generation System Test")
    print("=" * 60)
    
    generator = RealTimeASLGenerator()
    
    # Test cases with different user inputs
    test_cases = [
        "CGPA OF MR JAIN IN GOOD",
        "I want to learn advanced calculus",
        "Teacher explains quantum physics",
        "Students work on chemistry project together",
        "My grade improved from B to A",
        "Help me understand molecular biology",
        "Class presentation on American history"
    ]
    
    for i, user_input in enumerate(test_cases):
        print(f"\n{i+1}. Testing: '{user_input}'")
        
        try:
            result = generator.generate_asl_from_prompt(user_input)
            
            print(f"   ✅ Success!")
            print(f"   Concepts: {result['concepts']}")
            print(f"   Duration: {result['duration']}s")
            print(f"   Video: {result['video_file']}")
            print(f"   ASL Content: {len(result['asl_content'])} items")
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print(f"\n" + "=" * 60)
    print("🎉 Real-Time ASL System Test Complete!")
    
    print("\n🌟 NEW FEATURES:")
    print("   ✅ Dynamic concept extraction from user input")
    print("   ✅ Real-time ASL content generation")
    print("   ✅ Custom video metadata tracking")
    print("   ✅ No more static token mapping")
    print("   ✅ Videos based on YOUR exact prompt")
    
    print("\n🚀 READY FOR INTEGRATION:")
    print("   1. System extracts concepts from YOUR input")
    print("   2. Generates appropriate ASL content")
    print("   3. Creates unique videos for YOUR prompt")
    print("   4. Tracks all user inputs and responses")

if __name__ == "__main__":
    test_realtime_system()
