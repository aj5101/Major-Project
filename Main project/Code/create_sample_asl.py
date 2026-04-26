"""
Create Sample ASL Videos
Creates simple placeholder ASL videos for demonstration purposes.
"""

import os
import cv2
import numpy as np
from moviepy.editor import ImageSequenceClip, ColorClip
import json

def create_placeholder_asl_video(output_path, text, duration=2.0):
    """Create a simple placeholder ASL video with text"""
    
    # Create frames with text
    frames = []
    fps = 24
    num_frames = int(duration * fps)
    
    for i in range(num_frames):
        # Create a colored background
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        
        # Add gradient background
        for y in range(480):
            frame[y, :, 0] = int(100 + (155 * y / 480))  # Red gradient
            frame[y, :, 1] = int(50 + (100 * y / 480))   # Green gradient  
            frame[y, :, 2] = int(150 + (105 * y / 480))  # Blue gradient
        
        # Add text
        cv2.putText(frame, text, (320, 240), 
                   cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)
        
        # Add "ASL Sign" label
        cv2.putText(frame, "ASL Sign", (320, 400), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (200, 200, 200), 2)
        
        frames.append(frame)
    
    # Save as video
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (640, 480))
    
    for frame in frames:
        out.write(frame)
    
    out.release()
    print(f"Created: {output_path}")

def main():
    """Create sample ASL videos for common words"""
    
    # Common educational words
    asl_words = [
        "HELLO",
        "LEARN", 
        "TOGETHER",
        "BOOK",
        "SCHOOL",
        "TEACHER",
        "STUDENT",
        "QUESTION",
        "ANSWER",
        "KNOWLEDGE"
    ]
    
    output_dir = "/Users/arihantjain/Desktop/Main project/Code/datasets/sample"
    os.makedirs(output_dir, exist_ok=True)
    
    # Create videos
    video_files = []
    for word in asl_words:
        filename = f"{word.lower()}.mp4"
        filepath = os.path.join(output_dir, filename)
        create_placeholder_asl_video(filepath, word, duration=2.0)
        video_files.append(filename)
    
    # Create gloss mapping
    gloss_mapping = {filename: word.lower() for filename, word in zip(video_files, asl_words)}
    
    with open(os.path.join(output_dir, "gloss_mapping.json"), "w") as f:
        json.dump(gloss_mapping, f, indent=2)
    
    print(f"\nCreated {len(video_files)} sample ASL videos")
    print(f"Gloss mapping saved to: {output_dir}/gloss_mapping.json")
    
    # Display mapping
    print("\nGloss Mapping:")
    for filename, gloss in gloss_mapping.items():
        print(f"  {filename} -> {gloss}")

if __name__ == "__main__":
    main()
