"""
Create Realistic ASL Sign Videos
Creates videos that simulate actual ASL signing with hand movements and positions.
"""

import cv2
import numpy as np
import math

def draw_asl_hello(frame, t):
    """Draw HELLO sign in ASL - hand wave motion"""
    height, width = frame.shape[:2]
    center_x, center_y = width // 2, height // 2
    
    # Wave motion parameters
    wave_amplitude = 50
    wave_frequency = 2
    base_y = center_y
    
    # Calculate hand position with wave
    hand_x = center_x + int(wave_amplitude * math.sin(wave_frequency * t))
    hand_y = base_y
    
    # Draw arm
    cv2.line(frame, (center_x - 100, center_y + 100), (hand_x, hand_y), (139, 69, 19), 8)  # Brown arm
    
    # Draw hand with fingers
    cv2.circle(frame, (hand_x, hand_y), 30, (255, 220, 177), -1)  # Skin tone hand
    
    # Draw fingers (simplified)
    for i in range(4):
        finger_x = hand_x + (i - 1.5) * 8
        finger_y = hand_y - 25
        cv2.circle(frame, (int(finger_x), int(finger_y)), 4, (255, 220, 177), -1)
    
    # Draw "HELLO" text
    cv2.putText(frame, "HELLO", (center_x, center_y + 150), 
               cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3)

def draw_asl_learn(frame, t):
    """Draw LEARN sign in ASL - hand to head motion"""
    height, width = frame.shape[:2]
    center_x, center_y = width // 2, height // 2
    
    # Hand moves from side to head
    progress = min(t / 1.0, 1.0)  # 1 second motion
    hand_x = center_x - 100 + int(150 * progress)
    hand_y = center_y - 50 - int(50 * progress)
    
    # Draw arm
    cv2.line(frame, (center_x - 100, center_y + 100), (hand_x, hand_y), (139, 69, 19), 8)
    
    # Draw hand with L-shape (simplified ASL L)
    cv2.circle(frame, (hand_x, hand_y), 25, (255, 220, 177), -1)
    
    # Draw thumb and index finger in L shape
    cv2.circle(frame, (hand_x + 15, hand_y), 6, (255, 220, 177), -1)  # Thumb
    cv2.circle(frame, (hand_x, hand_y - 20), 6, (255, 220, 177), -1)  # Index finger
    
    # Draw "LEARN" text
    cv2.putText(frame, "LEARN", (center_x, center_y + 150), 
               cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3)

def draw_asl_together(frame, t):
    """Draw TOGETHER sign in ASL - both hands circling"""
    height, width = frame.shape[:2]
    center_x, center_y = width // 2, height // 2
    
    # Circular motion for both hands
    radius = 60
    angle1 = t * 2 * math.pi  # Full circle
    angle2 = angle1 + math.pi  # Opposite hand
    
    # Left hand position
    hand1_x = center_x + int(radius * math.cos(angle1))
    hand1_y = center_y + int(radius * math.sin(angle1))
    
    # Right hand position  
    hand2_x = center_x + int(radius * math.cos(angle2))
    hand2_y = center_y + int(radius * math.sin(angle2))
    
    # Draw arms
    cv2.line(frame, (center_x - 100, center_y + 100), (hand1_x, hand1_y), (139, 69, 19), 6)
    cv2.line(frame, (center_x + 100, center_y + 100), (hand2_x, hand2_y), (139, 69, 19), 6)
    
    # Draw both hands
    cv2.circle(frame, (hand1_x, hand1_y), 25, (255, 220, 177), -1)
    cv2.circle(frame, (hand2_x, hand2_y), 25, (255, 220, 177), -1)
    
    # Draw fingers on both hands
    for hand_x, hand_y in [(hand1_x, hand1_y), (hand2_x, hand2_y)]:
        for i in range(4):
            finger_x = hand_x + (i - 1.5) * 6
            finger_y = hand_y - 20
            cv2.circle(frame, (int(finger_x), int(finger_y)), 3, (255, 220, 177), -1)
    
    # Draw "TOGETHER" text
    cv2.putText(frame, "TOGETHER", (center_x, center_y + 150), 
               cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3)

def create_realistic_asl_video(output_path, sign_type, duration=2.0):
    """Create a realistic ASL signing video"""
    
    frames = []
    fps = 30
    num_frames = int(duration * fps)
    
    # Sign drawing functions
    sign_functions = {
        'hello': draw_asl_hello,
        'learn': draw_asl_learn,
        'together': draw_asl_together
    }
    
    draw_function = sign_functions.get(sign_type.lower(), draw_asl_hello)
    
    for i in range(num_frames):
        # Create clean background
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        
        # Add subtle gradient background
        for y in range(480):
            frame[y, :, 0] = int(30 + (50 * y / 480))   # Red
            frame[y, :, 1] = int(40 + (60 * y / 480))   # Green  
            frame[y, :, 2] = int(60 + (80 * y / 480))   # Blue
        
        # Add grid lines for depth perception
        for x in range(0, 640, 40):
            cv2.line(frame, (x, 0), (x, 480), (50, 50, 50), 1)
        for y in range(0, 480, 40):
            cv2.line(frame, (0, y), (640, y), (50, 50, 50), 1)
        
        # Draw the ASL sign with animation
        t = i / fps  # Time in seconds
        draw_function(frame, t)
        
        # Add frame counter
        cv2.putText(frame, f"Frame: {i+1}/{num_frames}", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
        
        frames.append(frame)
    
    # Save as video
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (640, 480))
    
    for frame in frames:
        out.write(frame)
    
    out.release()
    print(f"Created realistic ASL video: {output_path}")

def main():
    """Create realistic ASL videos for all signs"""
    
    signs = ['hello', 'learn', 'together']
    output_dir = "/Users/arihantjain/Desktop/Main project/Code/datasets/realistic_asl"
    
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    for sign in signs:
        output_path = os.path.join(output_dir, f"{sign}_realistic.mp4")
        create_realistic_asl_video(output_path, sign, duration=2.0)
    
    print(f"\nCreated {len(signs)} realistic ASL videos in {output_dir}")

if __name__ == "__main__":
    main()
