"""
Dynamic ASL Video Generator
Creates custom ASL videos on-demand based on input text and required signs.
"""

from moviepy.editor import VideoFileClip, concatenate_videoclips
import os
import tempfile
import json
import re

class DynamicASLGenerator:
    """Generates custom ASL videos based on text input"""
    
    def __init__(self):
        _root = os.path.dirname(os.path.abspath(__file__))
        self.base_path = os.getenv("ASL_CLIPS_PATH", os.path.join(_root, "storage", "asl_clips"))
        self.output_path = os.getenv("ASL_OUTPUT_PATH", os.path.join(_root, "storage", "processed", "dynamic"))
        os.makedirs(self.output_path, exist_ok=True)
        
        # Available ASL videos
        self.available_signs = {
            'hello': [],
            'learn': [],
            'together': [],
            'book': [],
            'school': [],
            'teacher': [],
            'student': [],
            'question': [],
            'answer': [],
            'knowledge': [],
            'science': [],
            'math': []
        }
        
        # Load available video files
        self._load_video_files()
    
    def _load_video_files(self):
        """Load all available ASL video files"""
        if os.path.exists(self.base_path):
            for file in os.listdir(self.base_path):
                if file.endswith('.mp4'):
                    # Extract sign name from filename
                    sign_name = None
                    for sign in self.available_signs:
                        if file.lower().startswith(sign):
                            sign_name = sign
                            break
                    
                    if sign_name:
                        full_path = os.path.join(self.base_path, file)
                        self.available_signs[sign_name].append(full_path)
        
        # Sort files by modification time (newest first)
        for sign in self.available_signs:
            self.available_signs[sign].sort(key=os.path.getmtime, reverse=True)
    
    def extract_signs_from_text(self, text):
        """Extract ASL signs from input text"""
        word_to_sign = {
            # Greetings
            'hello': 'hello', 'hi': 'hello', 'hey': 'hello',
            'good': 'hello', 'morning': 'hello', 'welcome': 'hello',
            
            # Learning verbs
            'learn': 'learn', 'learning': 'learn', 'study': 'learn', 'studying': 'learn',
            'teach': 'teacher', 'teaching': 'teacher', 'education': 'learn',
            
            # Social concepts
            'together': 'together', 'group': 'together', 'team': 'together',
            'class': 'school', 'classroom': 'school',
            
            # Educational nouns
            'book': 'book', 'books': 'book', 'reading': 'book',
            'school': 'school', 'schools': 'school',
            'teacher': 'teacher', 'teachers': 'teacher', 'instructor': 'teacher',
            'student': 'student', 'students': 'student', 'pupil': 'student',
            
            # Question/Answer
            'question': 'question', 'questions': 'question', 'ask': 'question',
            'answer': 'answer', 'answers': 'answer', 'respond': 'answer',
            
            # Knowledge concepts
            'knowledge': 'knowledge', 'know': 'knowledge', 'understand': 'knowledge',
            'understanding': 'knowledge', 'smart': 'knowledge', 'intelligent': 'knowledge',
            
            # Subjects
            'science': 'science', 'scientific': 'science',
            'math': 'math', 'mathematics': 'math', 'calculate': 'math',
            
            # Achievement words
            'good': 'hello', 'great': 'hello', 'excellent': 'hello',
            'performance': 'hello', 'grade': 'student', 'grades': 'student',
            'cgpa': 'math', 'gpa': 'math', 'score': 'math',
            
            # Common school terms
            'mr': 'teacher', 'mister': 'teacher', 'sir': 'teacher',
            'jain': 'student', 'name': 'student', 'friend': 'student',
            
            # Additional words
            'cgpa': 'math', 'of': 'hello', 'in': 'hello', 'is': 'hello',
            'mister': 'teacher', 'sir': 'teacher'
        }
        
        words = re.findall(r'\b\w+\b', text.lower())
        signs = []
        
        for word in words:
            if word in word_to_sign:
                sign = word_to_sign[word]
                if sign in self.available_signs and sign not in signs:
                    signs.append(sign)
        
        return signs if signs else ['hello', 'learn', 'together']  # Default fallback
    
    def create_custom_video(self, text, video_id=None):
        """Create a custom ASL video for the given text"""
        print(f"Creating custom ASL video for: '{text}'")
        
        # Extract signs from text
        signs = self.extract_signs_from_text(text)
        print(f"Signs needed: {signs}")
        
        # Get video paths for each sign
        video_paths = []
        for sign in signs:
            if self.available_signs[sign]:
                # Use the newest video for this sign
                video_paths.append(self.available_signs[sign][0])
            else:
                print(f"Warning: No video found for sign '{sign}'")
        
        if not video_paths:
            raise ValueError("No video files available for the required signs")
        
        # Generate unique filename
        if video_id is None:
            import hashlib
            video_id = hashlib.md5(f"{text}_{len(signs)}".encode()).hexdigest()[:8]
        
        output_filename = f"custom_{video_id}.mp4"
        output_filepath = os.path.join(self.output_path, output_filename)
        
        # Check if video already exists
        if os.path.exists(output_filepath):
            print(f"Video already exists: {output_filepath}")
            return {
                'video_file': output_filename,
                'signs': signs,
                'duration': self._get_video_duration(output_filepath),
                'text': text
            }
        
        # Load and stitch videos
        clips = []
        for i, video_path in enumerate(video_paths):
            if os.path.exists(video_path):
                clip = VideoFileClip(video_path)
                clips.append(clip)
                print(f"Loaded clip {i+1}: {os.path.basename(video_path)}")
            else:
                print(f"Video not found: {video_path}")
        
        if not clips:
            raise ValueError("No valid video clips to stitch")
        
        # Concatenate clips
        print("Stitching clips together...")
        final_clip = concatenate_videoclips(clips, method="compose")
        
        # Write final video
        print(f"Writing custom video to {output_filepath}...")
        final_clip.write_videofile(
            output_filepath,
            fps=30,
            codec='libx264',
            audio_codec='aac',
            verbose=False,
            logger=None
        )
        
        print(f"Custom ASL video created: {output_filepath}")
        print(f"Total duration: {final_clip.duration}s")
        
        # Clean up
        final_clip.close()
        for clip in clips:
            clip.close()
        
        return {
            'video_file': output_filename,
            'signs': signs,
            'duration': final_clip.duration,
            'text': text
        }
    
    def _get_video_duration(self, video_path):
        """Get duration of a video file"""
        try:
            clip = VideoFileClip(video_path)
            duration = clip.duration
            clip.close()
            return duration
        except:
            return 0.0
    
    def get_video_info(self, video_file):
        """Get information about a generated video"""
        video_path = os.path.join(self.output_path, video_file)
        if os.path.exists(video_path):
            return {
                'file': video_file,
                'path': video_path,
                'duration': self._get_video_duration(video_path),
                'size': os.path.getsize(video_path)
            }
        return None

# Global instance
generator = DynamicASLGenerator()

def create_video_for_text(text, video_id=None):
    """Convenience function to create video for text"""
    return generator.create_custom_video(text, video_id)

def get_available_signs():
    """Get list of available ASL signs"""
    return list(generator.available_signs.keys())

if __name__ == "__main__":
    # Test the generator
    test_texts = [
        "Hello students welcome to class",
        "Science helps us understand the world",
        "Teacher asks question student answers",
        "Books help us gain knowledge",
        "Math teaches us to solve problems"
    ]
    
    for text in test_texts:
        try:
            result = create_video_for_text(text)
            print(f"✅ Created: {text}")
            print(f"   Video: {result['video_file']}")
            print(f"   Signs: {result['signs']}")
            print(f"   Duration: {result['duration']:.1f}s")
            print()
        except Exception as e:
            print(f"❌ Failed: {text} - {e}")
