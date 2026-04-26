"""
Speech-to-Text Module

Uses OpenAI Whisper to convert audio/video speech to text.
Supports multiple languages and handles various audio qualities.
"""

import whisper
import os
from moviepy.editor import VideoFileClip
import tempfile
import ssl
import urllib.request

class SpeechToText:
    """
    Speech-to-text converter using OpenAI Whisper.
    
    Whisper is a state-of-the-art speech recognition model that works
    well with various accents and audio qualities, making it suitable
    for children's content.
    """
    
    def __init__(self, model_name: str = "base"):
        """
        Initialize Whisper model.
        
        Args:
            model_name: Whisper model size (tiny, base, small, medium, large)
                       Larger models are more accurate but slower.
        """
        self.model_name = os.getenv("WHISPER_MODEL", model_name)
        print(f"Loading Whisper model: {self.model_name}")
        
        # Fix SSL certificate issues for model download
        # Force urllib/ssl to skip verification (corp/self-signed proxies)
        ssl._create_default_https_context = ssl._create_unverified_context  # type: ignore[attr-defined]

        # Create unverified SSL context for model downloads
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE

        # Temporarily disable SSL verification for urllib requests
        opener = urllib.request.build_opener(urllib.request.HTTPSHandler(context=ssl_context))
        urllib.request.install_opener(opener)

        try:
            self.model = whisper.load_model(self.model_name)
            print("Whisper model loaded successfully")
        except Exception as e:
            print(f"Error loading Whisper model: {e}")
            print("Attempting to continue with model download (SSL disabled)...")
            # Retry once more
            self.model = whisper.load_model(self.model_name)
            print("Whisper model loaded successfully after retry")
    
    async def transcribe(self, video_path: str) -> str:
        """
        Extract audio from video and transcribe to text.
        
        Args:
            video_path: Path to video file
            
        Returns:
            transcribed_text: Full transcribed text
        """
        try:
            # Extract audio from video
            audio_path = await self._extract_audio(video_path)
            
            # Transcribe audio
            print(f"Transcribing audio from {video_path}")
            result = self.model.transcribe(
                audio_path,
                language="en",  # Can be made configurable
                task="transcribe"
            )
            
            # Clean up temporary audio file
            if os.path.exists(audio_path) and audio_path.startswith(tempfile.gettempdir()):
                os.remove(audio_path)
            
            transcribed_text = result["text"].strip()
            print(f"Transcription completed: {len(transcribed_text)} characters")
            
            return transcribed_text
            
        except Exception as e:
            print(f"Error in transcription: {e}")
            raise
    
    async def _extract_audio(self, video_path: str) -> str:
        """
        Extract audio track from video file.
        
        Args:
            video_path: Path to video file
            
        Returns:
            audio_path: Path to extracted audio file (temporary)
        """
        try:
            # Create temporary audio file
            temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
            temp_audio_path = temp_audio.name
            temp_audio.close()
            
            # Extract audio using moviepy
            video = VideoFileClip(video_path)
            audio = video.audio
            
            if audio is None:
                raise ValueError("No audio track found in video")
            
            # Write audio to temporary file
            audio.write_audiofile(temp_audio_path, verbose=False, logger=None)
            
            # Clean up
            video.close()
            audio.close()
            
            return temp_audio_path
            
        except Exception as e:
            print(f"Error extracting audio: {e}")
            raise

