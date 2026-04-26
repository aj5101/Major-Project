"""
Create Comprehensive ASL Sign Library
Creates realistic ASL videos for common educational words.
"""

import cv2
import numpy as np
import math
import os

def draw_asl_hello(frame, t):
    """HELLO sign - waving hand"""
    height, width = frame.shape[:2]
    center_x, center_y = width // 2, height // 2
    
    wave_amplitude = 50
    wave_frequency = 2
    hand_x = center_x + int(wave_amplitude * math.sin(wave_frequency * t))
    hand_y = center_y
    
    cv2.line(frame, (center_x - 100, center_y + 100), (hand_x, hand_y), (139, 69, 19), 8)
    cv2.circle(frame, (hand_x, hand_y), 30, (255, 220, 177), -1)
    
    # Fingers
    for i in range(4):
        finger_x = hand_x + (i - 1.5) * 8
        finger_y = hand_y - 25
        cv2.circle(frame, (int(finger_x), int(finger_y)), 4, (255, 220, 177), -1)
    
    cv2.putText(frame, "HELLO", (center_x, center_y + 150), 
               cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3)

def draw_asl_learn(frame, t):
    """LEARN sign - hand to head"""
    height, width = frame.shape[:2]
    center_x, center_y = width // 2, height // 2
    
    progress = min(t / 1.0, 1.0)
    hand_x = center_x - 100 + int(150 * progress)
    hand_y = center_y - 50 - int(50 * progress)
    
    cv2.line(frame, (center_x - 100, center_y + 100), (hand_x, hand_y), (139, 69, 19), 8)
    cv2.circle(frame, (hand_x, hand_y), 25, (255, 220, 177), -1)
    
    # L-shape
    cv2.circle(frame, (hand_x + 15, hand_y), 6, (255, 220, 177), -1)
    cv2.circle(frame, (hand_x, hand_y - 20), 6, (255, 220, 177), -1)
    
    cv2.putText(frame, "LEARN", (center_x, center_y + 150), 
               cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3)

def draw_asl_together(frame, t):
    """TOGETHER sign - both hands circling"""
    height, width = frame.shape[:2]
    center_x, center_y = width // 2, height // 2
    
    radius = 60
    angle1 = t * 2 * math.pi
    angle2 = angle1 + math.pi
    
    hand1_x = center_x + int(radius * math.cos(angle1))
    hand1_y = center_y + int(radius * math.sin(angle1))
    hand2_x = center_x + int(radius * math.cos(angle2))
    hand2_y = center_y + int(radius * math.sin(angle2))
    
    cv2.line(frame, (center_x - 100, center_y + 100), (hand1_x, hand1_y), (139, 69, 19), 6)
    cv2.line(frame, (center_x + 100, center_y + 100), (hand2_x, hand2_y), (139, 69, 19), 6)
    
    cv2.circle(frame, (hand1_x, hand1_y), 25, (255, 220, 177), -1)
    cv2.circle(frame, (hand2_x, hand2_y), 25, (255, 220, 177), -1)
    
    # Fingers
    for hand_x, hand_y in [(hand1_x, hand1_y), (hand2_x, hand2_y)]:
        for i in range(4):
            finger_x = hand_x + (i - 1.5) * 6
            finger_y = hand_y - 20
            cv2.circle(frame, (int(finger_x), int(finger_y)), 3, (255, 220, 177), -1)
    
    cv2.putText(frame, "TOGETHER", (center_x, center_y + 150), 
               cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3)

def draw_asl_book(frame, t):
    """BOOK sign - opening hands like book"""
    height, width = frame.shape[:2]
    center_x, center_y = width // 2, height // 2
    
    # Opening motion
    progress = min(t / 1.0, 1.0)
    hand_separation = int(80 * progress)
    
    # Left hand
    left_x = center_x - 40 - hand_separation // 2
    right_x = center_x + 40 + hand_separation // 2
    
    cv2.line(frame, (center_x - 100, center_y + 100), (left_x, center_y), (139, 69, 19), 6)
    cv2.line(frame, (center_x + 100, center_y + 100), (right_x, center_y), (139, 69, 19), 6)
    
    cv2.circle(frame, (left_x, center_y), 25, (255, 220, 177), -1)
    cv2.circle(frame, (right_x, center_y), 25, (255, 220, 177), -1)
    
    # Fingers spread like pages
    for hand_x in [left_x, right_x]:
        for i in range(5):
            finger_x = hand_x + (i - 2) * 5
            finger_y = center_y - 20
            cv2.circle(frame, (int(finger_x), int(finger_y)), 3, (255, 220, 177), -1)
    
    cv2.putText(frame, "BOOK", (center_x, center_y + 150), 
               cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3)

def draw_asl_school(frame, t):
    """SCHOOL sign - clapping motion"""
    height, width = frame.shape[:2]
    center_x, center_y = width // 2, height // 2
    
    # Clapping motion
    progress = (t % 0.5) * 2  # Repeat every 0.5 seconds
    hand_separation = int(60 * (1 - progress))
    
    left_x = center_x - hand_separation // 2
    right_x = center_x + hand_separation // 2
    
    cv2.line(frame, (center_x - 100, center_y + 100), (left_x, center_y), (139, 69, 19), 6)
    cv2.line(frame, (center_x + 100, center_y + 100), (right_x, center_y), (139, 69, 19), 6)
    
    cv2.circle(frame, (left_x, center_y), 25, (255, 220, 177), -1)
    cv2.circle(frame, (right_x, center_y), 25, (255, 220, 177), -1)
    
    # All fingers extended
    for hand_x in [left_x, right_x]:
        for i in range(5):
            finger_x = hand_x + (i - 2) * 5
            finger_y = center_y - 25
            cv2.circle(frame, (int(finger_x), int(finger_y)), 3, (255, 220, 177), -1)
    
    cv2.putText(frame, "SCHOOL", (center_x, center_y + 150), 
               cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3)

def draw_asl_teacher(frame, t):
    """TEACHER sign - pointing to head"""
    height, width = frame.shape[:2]
    center_x, center_y = width // 2, height // 2
    
    # Pointing motion
    progress = min(t / 0.8, 1.0)
    hand_x = center_x
    hand_y = center_y - 50 - int(30 * progress)
    
    cv2.line(frame, (center_x, center_y + 100), (hand_x, hand_y), (139, 69, 19), 6)
    cv2.circle(frame, (hand_x, hand_y), 25, (255, 220, 177), -1)
    
    # Index finger pointing
    cv2.circle(frame, (hand_x, hand_y - 20), 6, (255, 220, 177), -1)
    
    # Other fingers folded
    for i in [-2, -1, 1, 2]:
        finger_x = hand_x + i * 6
        finger_y = hand_y + 5
        cv2.circle(frame, (int(finger_x), int(finger_y)), 3, (255, 220, 177), -1)
    
    cv2.putText(frame, "TEACHER", (center_x, center_y + 150), 
               cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3)

def draw_asl_student(frame, t):
    """STUDENT sign - person at desk"""
    height, width = frame.shape[:2]
    center_x, center_y = width // 2, height // 2
    
    # Sitting motion
    progress = min(t / 1.0, 1.0)
    sit_height = int(30 * progress)
    
    # Body
    cv2.rectangle(frame, (center_x - 15, center_y - 30 + sit_height), 
                  (center_x + 15, center_y + 30 + sit_height), (100, 100, 200), -1)
    
    # Head
    cv2.circle(frame, (center_x, center_y - 45 + sit_height), 15, (255, 220, 177), -1)
    
    # Desk
    cv2.rectangle(frame, (center_x - 40, center_y + 30 + sit_height), 
                  (center_x + 40, center_y + 40 + sit_height), (139, 69, 19), -1)
    
    cv2.putText(frame, "STUDENT", (center_x, center_y + 150), 
               cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3)

def draw_asl_question(frame, t):
    """QUESTION sign - questioning gesture"""
    height, width = frame.shape[:2]
    center_x, center_y = width // 2, height // 2
    
    # Questioning motion - hand to face
    progress = min(t / 0.8, 1.0)
    hand_x = center_x - 60
    hand_y = center_y - 20 + int(20 * math.sin(progress * math.pi))
    
    cv2.line(frame, (center_x - 100, center_y + 100), (hand_x, hand_y), (139, 69, 19), 6)
    cv2.circle(frame, (hand_x, hand_y), 25, (255, 220, 177), -1)
    
    # Question mark hand shape
    cv2.circle(frame, (hand_x, hand_y - 20), 6, (255, 220, 177), -1)
    
    # Eyebrows raised (questioning expression)
    cv2.line(frame, (center_x - 30, center_y - 60), (center_x - 10, center_y - 65), (255, 255, 255), 2)
    cv2.line(frame, (center_x + 10, center_y - 65), (center_x + 30, center_y - 60), (255, 255, 255), 2)
    
    cv2.putText(frame, "QUESTION", (center_x, center_y + 150), 
               cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3)

def draw_asl_answer(frame, t):
    """ANSWER sign - open hand presentation"""
    height, width = frame.shape[:2]
    center_x, center_y = width // 2, height // 2
    
    # Presenting motion
    progress = min(t / 1.0, 1.0)
    hand_x = center_x + int(40 * progress)
    hand_y = center_y
    
    cv2.line(frame, (center_x - 100, center_y + 100), (hand_x, hand_y), (139, 69, 19), 6)
    cv2.circle(frame, (hand_x, hand_y), 30, (255, 220, 177), -1)
    
    # Open hand - all fingers extended
    for i in range(5):
        finger_x = hand_x + (i - 2) * 6
        finger_y = hand_y - 25
        cv2.circle(frame, (int(finger_x), int(finger_y)), 4, (255, 220, 177), -1)
    
    cv2.putText(frame, "ANSWER", (center_x, center_y + 150), 
               cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3)

def draw_asl_knowledge(frame, t):
    """KNOWLEDGE sign - brain/head tap"""
    height, width = frame.shape[:2]
    center_x, center_y = width // 2, height // 2
    
    # Tapping motion
    progress = (t % 0.4) * 2.5  # Tap every 0.4 seconds
    tap_offset = int(10 * math.sin(progress * math.pi))
    
    hand_x = center_x
    hand_y = center_y - 50 + tap_offset
    
    cv2.line(frame, (center_x, center_y + 100), (hand_x, hand_y), (139, 69, 19), 6)
    cv2.circle(frame, (hand_x, hand_y), 25, (255, 220, 177), -1)
    
    # All fingers touching head
    for i in range(5):
        finger_x = hand_x + (i - 2) * 5
        finger_y = hand_y - 20
        cv2.circle(frame, (int(finger_x), int(finger_y)), 3, (255, 220, 177), -1)
    
    # Brain symbol
    cv2.circle(frame, (center_x, center_y - 70), 20, (200, 200, 255), 2)
    
    cv2.putText(frame, "KNOWLEDGE", (center_x, center_y + 150), 
               cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3)

def draw_asl_science(frame, t):
    """SCIENCE sign - experimenting gesture"""
    height, width = frame.shape[:2]
    center_x, center_y = width // 2, height // 2
    
    # Experimenting motion - mixing
    progress = t * 2 * math.pi
    hand1_x = center_x - 30 + int(20 * math.cos(progress))
    hand1_y = center_y + int(10 * math.sin(progress))
    hand2_x = center_x + 30 + int(20 * math.cos(progress + math.pi))
    hand2_y = center_y + int(10 * math.sin(progress + math.pi))
    
    cv2.line(frame, (center_x - 100, center_y + 100), (hand1_x, hand1_y), (139, 69, 19), 6)
    cv2.line(frame, (center_x + 100, center_y + 100), (hand2_x, hand2_y), (139, 69, 19), 6)
    
    cv2.circle(frame, (hand1_x, hand1_y), 25, (255, 220, 177), -1)
    cv2.circle(frame, (hand2_x, hand2_y), 25, (255, 220, 177), -1)
    
    # Beaker shape between hands
    cv2.rectangle(frame, (center_x - 10, center_y - 20), (center_x + 10, center_y + 20), (100, 200, 255), -1)
    
    cv2.putText(frame, "SCIENCE", (center_x, center_y + 150), 
               cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3)

def draw_asl_math(frame, t):
    """MATH sign - counting/calculating"""
    height, width = frame.shape[:2]
    center_x, center_y = width // 2, height // 2
    
    # Counting motion
    finger_count = int(t * 2) % 6  # Count 0-5 fingers
    if finger_count > 5:
        finger_count = 5
    
    hand_x = center_x
    hand_y = center_y
    
    cv2.line(frame, (center_x, center_y + 100), (hand_x, hand_y), (139, 69, 19), 6)
    cv2.circle(frame, (hand_x, hand_y), 30, (255, 220, 177), -1)
    
    # Show finger count
    if finger_count == 0:
        # Fist
        cv2.circle(frame, (hand_x, hand_y), 25, (255, 220, 177), -1)
    else:
        # Extended fingers
        for i in range(finger_count):
            finger_x = hand_x + (i - finger_count/2 + 0.5) * 8
            finger_y = hand_y - 25
            cv2.circle(frame, (int(finger_x), int(finger_y)), 4, (255, 220, 177), -1)
    
    # Numbers floating
    for i, num in enumerate(['1', '2', '3', '+', '=']):
        num_x = center_x - 40 + i * 20
        num_y = center_y - 80
        cv2.putText(frame, num, (num_x, num_y), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 200), 2)
    
    cv2.putText(frame, "MATH", (center_x, center_y + 150), 
               cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3)

def create_asl_video(output_path, sign_type, duration=2.0):
    """Create an ASL signing video"""
    
    frames = []
    fps = 30
    num_frames = int(duration * fps)
    
    # Sign drawing functions
    sign_functions = {
        'hello': draw_asl_hello,
        'learn': draw_asl_learn,
        'together': draw_asl_together,
        'book': draw_asl_book,
        'school': draw_asl_school,
        'teacher': draw_asl_teacher,
        'student': draw_asl_student,
        'question': draw_asl_question,
        'answer': draw_asl_answer,
        'knowledge': draw_asl_knowledge,
        'science': draw_asl_science,
        'math': draw_asl_math
    }
    
    draw_function = sign_functions.get(sign_type.lower(), draw_asl_hello)
    
    for i in range(num_frames):
        # Create clean background
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        
        # Add subtle gradient background
        for y in range(480):
            frame[y, :, 0] = int(30 + (50 * y / 480))
            frame[y, :, 1] = int(40 + (60 * y / 480))
            frame[y, :, 2] = int(60 + (80 * y / 480))
        
        # Add grid lines
        for x in range(0, 640, 40):
            cv2.line(frame, (x, 0), (x, 480), (50, 50, 50), 1)
        for y in range(0, 480, 40):
            cv2.line(frame, (0, y), (640, y), (50, 50, 50), 1)
        
        # Draw the ASL sign with animation
        t = i / fps
        draw_function(frame, t)
        
        frames.append(frame)
    
    # Save as video
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (640, 480))
    
    for frame in frames:
        out.write(frame)
    
    out.release()
    print(f"Created ASL video: {output_path}")

def main():
    """Create comprehensive ASL video library"""
    
    signs = [
        'hello', 'learn', 'together', 'book', 'school', 
        'teacher', 'student', 'question', 'answer', 
        'knowledge', 'science', 'math'
    ]
    
    output_dir = "/Users/arihantjain/Desktop/Main project/Code/datasets/comprehensive_asl"
    os.makedirs(output_dir, exist_ok=True)
    
    for sign in signs:
        output_path = os.path.join(output_dir, f"{sign}.mp4")
        create_asl_video(output_path, sign, duration=2.0)
    
    print(f"\nCreated {len(signs)} comprehensive ASL videos in {output_dir}")

if __name__ == "__main__":
    main()
