"""
Video Processing and Stitching Module

Stitches multiple ASL video clips together into a single narration video.
Handles transitions, timing, and video encoding.
"""

import os
from moviepy.editor import VideoFileClip, concatenate_videoclips
import cv2

class VideoStitcher:
    """
    Stitches ASL video clips into a single narration video.
    
    Handles:
    - Concatenating clips in sequence
    - Ensuring consistent resolution and frame rate
    - Adding smooth transitions (optional)
    - Encoding final video
    """
    
    def __init__(self):
        """Initialize video stitcher"""
        self.target_fps = 30
        self.target_resolution = (640, 480)  # Standard resolution for ASL videos
    
    async def stitch_clips(self, clip_paths: list, output_path: str, transition_duration: float = 0.0):
        """
        Stitch multiple ASL video clips into one video.
        
        Args:
            clip_paths: List of paths to ASL video clips
            output_path: Path to save final stitched video
            transition_duration: Duration of transition between clips (0 = no transition)
        """
        if not clip_paths:
            raise ValueError("No clips provided for stitching")
        
        print(f"Stitching {len(clip_paths)} clips into {output_path}")
        
        clips = []
        
        try:
            # Load and prepare each clip
            for i, clip_path in enumerate(clip_paths):
                if not os.path.exists(clip_path):
                    print(f"Warning: Clip not found: {clip_path}, skipping")
                    continue
                
                try:
                    clip = VideoFileClip(clip_path)
                    
                    # Resize to target resolution if needed
                    if clip.size != self.target_resolution:
                        clip = clip.resize(self.target_resolution)
                    
                    # Set consistent FPS
                    if clip.fps != self.target_fps:
                        clip = clip.set_fps(self.target_fps)
                    
                    clips.append(clip)
                    print(f"Loaded clip {i+1}/{len(clip_paths)}: {clip_path}")
                    
                except Exception as e:
                    print(f"Error loading clip {clip_path}: {e}")
                    continue
            
            if not clips:
                raise ValueError("No valid clips to stitch")
            
            # Concatenate clips
            print("Concatenating clips...")
            final_clip = concatenate_videoclips(clips, method="compose")
            
            # Ensure output directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Write final video
            print(f"Writing final video to {output_path}...")
            final_clip.write_videofile(
                output_path,
                fps=self.target_fps,
                codec='libx264',
                audio_codec='aac',
                preset='medium',
                verbose=False,
                logger=None
            )
            
            print(f"Video stitching completed: {output_path}")
            
            # Clean up
            final_clip.close()
            for clip in clips:
                clip.close()
            
        except Exception as e:
            print(f"Error stitching videos: {e}")
            # Clean up on error
            for clip in clips:
                try:
                    clip.close()
                except:
                    pass
            raise
    
    def get_video_info(self, video_path: str) -> dict:
        """
        Get information about a video file.
        
        Args:
            video_path: Path to video file
            
        Returns:
            Dictionary with video properties (fps, duration, resolution, etc.)
        """
        try:
            clip = VideoFileClip(video_path)
            info = {
                "fps": clip.fps,
                "duration": clip.duration,
                "size": clip.size,
                "has_audio": clip.audio is not None
            }
            clip.close()
            return info
        except Exception as e:
            print(f"Error getting video info: {e}")
            return {}

