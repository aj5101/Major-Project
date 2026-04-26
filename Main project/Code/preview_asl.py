"""
Preview ASL Video Information
"""

import cv2
import os

def preview_asl_videos():
    """Show information about the realistic ASL videos"""
    
    videos = [
        "/Users/arihantjain/Desktop/Main project/Code/storage/asl_clips/hello_970ffe78.mp4",
        "/Users/arihantjain/Desktop/Main project/Code/storage/asl_clips/learn_abf6d71a.mp4",
        "/Users/arihantjain/Desktop/Main project/Code/storage/asl_clips/together_66ae03fb.mp4"
    ]
    
    signs = ["HELLO", "LEARN", "TOGETHER"]
    
    print("🤟 Realistic ASL Video Preview")
    print("=" * 50)
    
    for i, (video_path, sign) in enumerate(zip(videos, signs)):
        if os.path.exists(video_path):
            cap = cv2.VideoCapture(video_path)
            
            # Get video info
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            duration = frame_count / fps if fps > 0 else 0
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            
            print(f"\n{i+1}. {sign} Sign:")
            print(f"   📹 Resolution: {width}x{height}")
            print(f"   ⏱️  Duration: {duration:.1f}s")
            print(f"   🎬 FPS: {fps}")
            print(f"   📊 Frames: {frame_count}")
            print(f"   🎯 Features: Animated hand movements, proper ASL positioning")
            
            cap.release()
        else:
            print(f"\n{i+1}. {sign}: Video not found")
    
    print("\n" + "=" * 50)
    print("🎭 What You'll See:")
    print("   • HELLO: Waving hand motion")
    print("   • LEARN: Hand moving to head (L-shape)")
    print("   • TOGETHER: Both hands circling")
    print("   • All signs: Proper ASL positioning and movement")
    print("   • Background: Grid for depth perception")
    
    print("\n🌐 Ready to View:")
    print("   Go to http://localhost:3000/upload")
    print("   Select '📝 Text Input' tab")
    print("   Enter any text and click 'Start ASL Text Processing'")
    print("   Watch the realistic ASL signing video!")

if __name__ == "__main__":
    preview_asl_videos()
