"""
Create a Test Video with Real Speech
"""

import cv2
import numpy as np
from moviepy.editor import ImageSequenceClip, AudioFileClip
import tempfile
import os

def create_test_video_with_speech(output_path, text="Hello learn together", duration=6.0):
    """Create a test video with visual text and real speech audio"""
    
    frames = []
    fps = 24
    num_frames = int(duration * fps)
    
    # Create frames with text
    for i in range(num_frames):
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        
        # Add gradient background
        for y in range(480):
            frame[y, :, 0] = int(50 + (100 * y / 480))
            frame[y, :, 1] = int(100 + (100 * y / 480))
            frame[y, :, 2] = int(150 + (105 * y / 480))
        
        # Add text
        cv2.putText(frame, text, (320, 240), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3)
        
        frames.append(frame)
    
    # Save frames as video
    temp_video = tempfile.NamedTemporaryFile(suffix='.mp4', delete=False)
    temp_video.close()
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(temp_video.name, fourcc, fps, (640, 480))
    
    for frame in frames:
        out.write(frame)
    
    out.close()
    
    # Create simple speech audio using text-to-speech (if available) or use a pre-recorded audio
    try:
        # Try to use gTTS for speech synthesis
        try:
            from gtts import gTTS
            tts = gTTS(text=text, lang='en', slow=False)
            temp_audio = tempfile.NamedTemporaryFile(suffix='.mp3', delete=False)
            temp_audio.close()
            tts.save(temp_audio.name)
            
            # Load video and audio
            video = ImageSequenceClip([frame for frame in frames], fps=fps)
            audio = AudioFileClip(temp_audio.name)
            
            # Set audio and save
            final_video = video.set_audio(audio)
            final_video.write_videofile(output_path, fps=fps, codec='libx264', audio_codec='aac')
            
            # Clean up
            os.remove(temp_video.name)
            os.remove(temp_audio.name)
            video.close()
            audio.close()
            final_video.close()
            
        except ImportError:
            print("gTTS not available, creating video without speech")
            # Just use the video without audio
            os.rename(temp_video.name, output_path)
            
    except Exception as e:
        print(f"Could not create speech audio: {e}")
        # Use the video without audio
        os.rename(temp_video.name, output_path)
    
    print(f"Created test video with speech: {output_path}")

if __name__ == "__main__":
    create_test_video_with_speech("test_speech_video.mp4", "Hello learn together", 6.0)
