"""
Test the ASL Video Processing Pipeline
Creates a simple test video and uploads it to demonstrate the full pipeline.
"""

import cv2
import numpy as np
import requests
import json
import time

def create_test_video(output_path, text="Hello, welcome to ASL learning!", duration=5.0):
    """Create a simple test video with text and silent audio"""
    
    frames = []
    fps = 24
    num_frames = int(duration * fps)
    
    for i in range(num_frames):
        # Create a colored background
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        
        # Add gradient background
        for y in range(480):
            frame[y, :, 0] = int(50 + (100 * y / 480))   # Red gradient
            frame[y, :, 1] = int(100 + (100 * y / 480))  # Green gradient  
            frame[y, :, 2] = int(150 + (105 * y / 480)) # Blue gradient
        
        # Add text
        cv2.putText(frame, text, (320, 240), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3)
        
        # Add "Educational Content" label
        cv2.putText(frame, "Educational Content", (320, 400), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (200, 200, 200), 2)
        
        frames.append(frame)
    
    # Save as video
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (640, 480))
    
    for frame in frames:
        out.write(frame)
    
    out.close()
    
    # Add silent audio using moviepy
    try:
        from moviepy.editor import VideoFileClip, AudioFileClip
        import numpy as np
        
        # Load the video
        video = VideoFileClip(output_path)
        
        # Create silent audio
        sample_rate = 44100
        duration = video.duration
        silent_audio = np.zeros((int(sample_rate * duration),), dtype=np.float32)
        
        # Save silent audio to temp file
        import tempfile
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_audio:
            import wave
            with wave.open(temp_audio.name, 'wb') as wav_file:
                wav_file.setnchannels(1)
                wav_file.setsampwidth(2)
                wav_file.setframerate(sample_rate)
                wav_file.writeframes(silent_audio.tobytes())
            
            # Add audio to video
            audio_clip = AudioFileClip(temp_audio.name)
            final_video = video.set_audio(audio_clip)
            final_video.write_videofile(output_path.replace('.mp4', '_with_audio.mp4'), codec='libx264', audio_codec='aac')
            
            # Replace original video
            import os
            os.remove(output_path)
            os.rename(output_path.replace('.mp4', '_with_audio.mp4'), output_path)
            
            # Clean up
            os.remove(temp_audio.name)
            
    except Exception as e:
        print(f"Warning: Could not add audio to video: {e}")
        # Continue without audio - the processing will fail but we can see the error
    
    print(f"Created test video: {output_path}")

def test_pipeline():
    """Test the complete ASL video processing pipeline"""
    
    print("🎬 Creating ASL Video Narration Platform Test")
    print("=" * 50)
    
    # 1. Create test video
    print("\n1. Creating test video...")
    create_test_video("test_education.mp4", "The dangers of road accidents", duration=3.0)
    
    # 2. Upload video
    print("\n2. Uploading video to backend...")
    with open("test_education.mp4", "rb") as f:
        files = {"file": f}
        response = requests.post("http://localhost:8000/api/videos/upload", files=files)
        
    if response.status_code == 200:
        upload_data = response.json()
        video_id = upload_data["video_id"]
        print(f"✅ Video uploaded successfully! ID: {video_id}")
    else:
        print(f"❌ Upload failed: {response.text}")
        return
    
    # 3. Start processing
    print("\n3. Starting video processing...")
    response = requests.post(f"http://localhost:8000/api/videos/{video_id}/process")
    
    if response.status_code == 200:
        print("✅ Processing started!")
    else:
        print(f"❌ Processing failed: {response.text}")
        return
    
    # 4. Monitor progress
    print("\n4. Monitoring processing progress...")
    max_attempts = 30  # Wait up to 2 minutes
    
    for attempt in range(max_attempts):
        response = requests.get(f"http://localhost:8000/api/videos/{video_id}/status")
        
        if response.status_code == 200:
            status_data = response.json()
            status = status_data["status"]
            progress = status_data.get("progress", 0)
            
            print(f"   Status: {status} | Progress: {progress*100:.1f}%")
            
            if status == "completed":
                print("✅ Processing completed!")
                break
            elif status == "failed":
                print(f"❌ Processing failed: {status_data.get('message', 'Unknown error')}")
                return
            
            time.sleep(4)  # Wait 4 seconds before checking again
        else:
            print(f"❌ Status check failed: {response.text}")
            return
    
    # 5. Get results
    print("\n5. Getting final results...")
    response = requests.get(f"http://localhost:8000/api/videos/{video_id}/result")
    
    if response.status_code == 200:
        result = response.json()
        print("✅ Results retrieved!")
        print(f"   Original Text: {result.get('original_text', 'N/A')}")
        print(f"   Simplified Text: {result.get('simplified_text', 'N/A')}")
        print(f"   ASL Clips: {len(result.get('asl_clips', []))} clips found")
        
        if result.get('asl_clips'):
            print("   ASL Clips Used:")
            for clip in result['asl_clips']:
                print(f"     - {clip.get('gloss', 'N/A')} (confidence: {clip.get('confidence', 0):.2f})")
    else:
        print(f"❌ Failed to get results: {response.text}")
    
    # 6. Show video URL
    video_url = f"http://localhost:8000/api/videos/{video_id}/asl-video"
    print(f"\n🎥 ASL Video URL: {video_url}")
    print(f"🌐 Frontend URL: http://localhost:3000/video/{video_id}")
    
    print("\n" + "=" * 50)
    print("🎉 Test completed! You can now:")
    print("   1. View the ASL video at the URL above")
    print("   2. See the results in the web interface")
    print("   3. Check the ASL clips that were matched")

if __name__ == "__main__":
    test_pipeline()
