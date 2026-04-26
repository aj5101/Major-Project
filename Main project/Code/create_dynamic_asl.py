"""
Dynamic ASL Text-to-Sign Mapping System
Maps input text to appropriate ASL signs and creates custom videos.
"""

from moviepy.editor import VideoFileClip, concatenate_videoclips
import os
import re
import json

class ASLTextMapper:
    """Maps text to ASL signs and creates custom videos"""
    
    def __init__(self):
        # Word-to-sign mapping
        self.word_to_sign = {
            # Greetings
            'hello': 'hello', 'hi': 'hello', 'hey': 'hello',
            
            # Learning verbs
            'learn': 'learn', 'learning': 'learn', 'study': 'learn', 'studying': 'learn',
            
            # Social concepts
            'together': 'together', 'group': 'together', 'team': 'together',
            
            # Educational nouns
            'book': 'book', 'books': 'book', 'reading': 'book',
            'school': 'school', 'schools': 'school', 'classroom': 'school',
            'teacher': 'teacher', 'teachers': 'teacher', 'instructor': 'teacher',
            'student': 'student', 'students': 'student', 'pupil': 'student',
            
            # Question/Answer
            'question': 'question', 'questions': 'question', 'ask': 'question',
            'answer': 'answer', 'answers': 'answer', 'respond': 'answer',
            
            # Knowledge concepts
            'knowledge': 'knowledge', 'know': 'knowledge', 'understand': 'knowledge',
            
            # Subjects
            'science': 'science', 'scientific': 'science',
            'math': 'math', 'mathematics': 'math', 'calculate': 'math',
            
            # Common educational words
            'education': 'learn', 'educational': 'learn',
            'teaching': 'teacher', 'instruction': 'teacher',
            'lessons': 'learn', 'lesson': 'learn',
            'class': 'school', 'classes': 'school',
            'academic': 'school', 'academics': 'school'
        }
        
        # Available signs in our dataset
        self.available_signs = [
            'hello', 'learn', 'together', 'book', 'school', 
            'teacher', 'student', 'question', 'answer', 
            'knowledge', 'science', 'math'
        ]
    
    def extract_signs_from_text(self, text):
        """Extract ASL signs from input text"""
        # Convert to lowercase and split into words
        words = re.findall(r'\b\w+\b', text.lower())
        
        signs = []
        for word in words:
            if word in self.word_to_sign:
                sign = self.word_to_sign[word]
                if sign in self.available_signs and sign not in signs:
                    signs.append(sign)
        
        return signs
    
    def get_video_paths_for_signs(self, signs):
        """Get video file paths for given signs"""
        base_path = "/Users/arihantjain/Desktop/Main project/Code/storage/asl_clips"
        
        # Get latest files for each sign
        video_paths = []
        for sign in signs:
            # Find the most recent file for this sign
            sign_files = []
            if os.path.exists(base_path):
                for file in os.listdir(base_path):
                    if file.startswith(sign) and file.endswith('.mp4'):
                        full_path = os.path.join(base_path, file)
                        sign_files.append(full_path)
            
            if sign_files:
                # Get the most recent file (by modification time)
                latest_file = max(sign_files, key=os.path.getmtime)
                video_paths.append(latest_file)
        
        return video_paths
    
    def create_custom_asl_video(self, text, output_path):
        """Create a custom ASL video based on input text"""
        print(f"Creating ASL video for: '{text}'")
        
        # Extract signs from text
        signs = self.extract_signs_from_text(text)
        
        if not signs:
            print("No matching signs found, using default signs")
            signs = ['hello', 'learn', 'together']  # Default fallback
        
        print(f"Signs to include: {signs}")
        
        # Get video paths
        video_paths = self.get_video_paths_for_signs(signs)
        
        if not video_paths:
            raise ValueError("No ASL video files found")
        
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
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Write final video
        print(f"Writing custom video to {output_path}...")
        final_clip.write_videofile(
            output_path,
            fps=30,
            codec='libx264',
            audio_codec='aac',
            verbose=False,
            logger=None
        )
        
        print(f"Custom ASL video created: {output_path}")
        print(f"Total duration: {final_clip.duration}s")
        print(f"Signs included: {signs}")
        
        # Clean up
        final_clip.close()
        for clip in clips:
            clip.close()
        
        return {
            'output_path': output_path,
            'signs': signs,
            'duration': final_clip.duration,
            'original_text': text
        }

def create_preset_videos():
    """Create preset videos for common educational phrases"""
    
    mapper = ASLTextMapper()
    
    # Common educational phrases
    phrases = [
        "Hello students welcome to class",
        "Let's learn science and math together",
        "Teacher asks question student answers",
        "Books help us gain knowledge",
        "School is where we learn together",
        "Hello teacher I want to learn",
        "Science helps us understand the world",
        "Math teaches us to solve problems",
        "Knowledge comes from asking questions",
        "Students and teachers learn together"
    ]
    
    output_dir = "/Users/arihantjain/Desktop/Main project/Code/storage/processed/preset_videos"
    os.makedirs(output_dir, exist_ok=True)
    
    results = []
    
    for i, phrase in enumerate(phrases):
        output_path = os.path.join(output_dir, f"phrase_{i+1:02d}.mp4")
        
        try:
            result = mapper.create_custom_asl_video(phrase, output_path)
            results.append({
                'phrase': phrase,
                'video_file': f"phrase_{i+1:02d}.mp4",
                'signs': result['signs'],
                'duration': result['duration']
            })
            print(f"✅ Created: {phrase}")
        except Exception as e:
            print(f"❌ Failed to create video for '{phrase}': {e}")
    
    # Save preset information
    preset_info = {
        'presets': results,
        'total_presets': len(results)
    }
    
    with open(os.path.join(output_dir, 'preset_info.json'), 'w') as f:
        json.dump(preset_info, f, indent=2)
    
    print(f"\nCreated {len(results)} preset videos")
    print(f"Preset info saved to: {output_dir}/preset_info.json")
    
    return results

if __name__ == "__main__":
    create_preset_videos()
