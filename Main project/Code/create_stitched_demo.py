"""
Create a stitched ASL demo video
"""

from moviepy.editor import VideoFileClip, concatenate_videoclips
import os

def create_stitched_demo():
    """Create a stitched ASL video from individual clips"""
    
    # Paths to our ASL clips
    clip_paths = [
        "/Users/arihantjain/Desktop/Main project/Code/storage/asl_clips/hello_f56a2e23.mp4",
        "/Users/arihantjain/Desktop/Main project/Code/storage/asl_clips/learn_281c86f4.mp4", 
        "/Users/arihantjain/Desktop/Main project/Code/storage/asl_clips/together_e72f2b98.mp4"
    ]
    
    # Load clips
    clips = []
    for clip_path in clip_paths:
        if os.path.exists(clip_path):
            clip = VideoFileClip(clip_path)
            clips.append(clip)
            print(f"Loaded: {clip_path} (duration: {clip.duration}s)")
    
    if clips:
        # Stitch them together
        print("Stitching clips...")
        final_clip = concatenate_videoclips(clips, method="compose")
        
        # Save the result
        output_path = "/Users/arihantjain/Desktop/Main project/Code/storage/processed/demo_stitched_asl.mp4"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        final_clip.write_videofile(
            output_path,
            fps=30,
            codec='libx264',
            audio_codec='aac',
            verbose=False,
            logger=None
        )
        
        print(f"Created stitched video: {output_path}")
        print(f"Total duration: {final_clip.duration}s")
        
        # Clean up
        final_clip.close()
        for clip in clips:
            clip.close()
    else:
        print("No clips found!")

if __name__ == "__main__":
    create_stitched_demo()
