"""
Create stitched video with realistic ASL signs
"""

from moviepy.editor import VideoFileClip, concatenate_videoclips
import os

def create_realistic_stitched_video():
    """Create a stitched ASL video with realistic signing"""
    
    # Get the latest realistic ASL clips
    clip_paths = [
        "/Users/arihantjain/Desktop/Main project/Code/storage/asl_clips/hello_970ffe78.mp4",
        "/Users/arihantjain/Desktop/Main project/Code/storage/asl_clips/learn_abf6d71a.mp4", 
        "/Users/arihantjain/Desktop/Main project/Code/storage/asl_clips/together_66ae03fb.mp4"
    ]
    
    # Load clips
    clips = []
    for i, clip_path in enumerate(clip_paths):
        if os.path.exists(clip_path):
            clip = VideoFileClip(clip_path)
            clips.append(clip)
            print(f"Loaded: {clip_path} (duration: {clip.duration}s)")
        else:
            print(f"Clip not found: {clip_path}")
    
    if clips:
        # Stitch them together
        print("Stitching realistic ASL clips...")
        final_clip = concatenate_videoclips(clips, method="compose")
        
        # Save the result
        output_path = "/Users/arihantjain/Desktop/Main project/Code/storage/processed/realistic_stitched_asl.mp4"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        final_clip.write_videofile(
            output_path,
            fps=30,
            codec='libx264',
            audio_codec='aac',
            verbose=False,
            logger=None
        )
        
        print(f"Created realistic stitched video: {output_path}")
        print(f"Total duration: {final_clip.duration}s")
        
        # Clean up
        final_clip.close()
        for clip in clips:
            clip.close()
        
        return output_path
    else:
        print("No clips found!")
        return None

if __name__ == "__main__":
    create_realistic_stitched_video()
