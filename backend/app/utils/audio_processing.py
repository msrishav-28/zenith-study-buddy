import io
import wave
import numpy as np
from typing import Tuple, Optional
import logging

logger = logging.getLogger(__name__)

class AudioProcessor:
    """Utilities for audio processing"""
    
    @staticmethod
    def validate_audio_format(audio_data: bytes) -> bool:
        """Validate if audio data is in correct format"""
        try:
            # Check if it's valid WAV format
            with io.BytesIO(audio_data) as audio_io:
                with wave.open(audio_io, 'rb') as wav_file:
                    # Check basic properties
                    channels = wav_file.getnchannels()
                    sample_width = wav_file.getsampwidth()
                    framerate = wav_file.getframerate()
                    
                    # Validate format
                    if channels not in [1, 2]:  # Mono or stereo
                        return False
                    if sample_width not in [1, 2, 4]:  # 8, 16, or 32 bit
                        return False
                    if framerate < 8000 or framerate > 48000:  # Common sample rates
                        return False
                    
                    return True
        except Exception as e:
            logger.error(f"Audio validation error: {e}")
            return False
    
    @staticmethod
    def get_audio_duration(audio_data: bytes) -> Optional[float]:
        """Get duration of audio in seconds"""
        try:
            with io.BytesIO(audio_data) as audio_io:
                with wave.open(audio_io, 'rb') as wav_file:
                    frames = wav_file.getnframes()
                    rate = wav_file.getframerate()
                    duration = frames / float(rate)
                    return duration
        except Exception as e:
            logger.error(f"Error getting audio duration: {e}")
            return None
    
   @staticmethod
    def normalize_audio(audio_data: bytes) -> bytes:
        """Normalize audio volume"""
        try:
            with io.BytesIO(audio_data) as input_io:
                with wave.open(input_io, 'rb') as wav_in:
                    params = wav_in.getparams()
                    frames = wav_in.readframes(params.nframes)
                    
                    # Handle different bit depths
                    if params.sampwidth == 1:
                        audio_array = np.frombuffer(frames, dtype=np.uint8)
                        max_val = 255
                    elif params.sampwidth == 2:
                        audio_array = np.frombuffer(frames, dtype=np.int16)
                        max_val = 32767
                    elif params.sampwidth == 4:
                        audio_array = np.frombuffer(frames, dtype=np.int32)
                        max_val = 2147483647
                    else:
                        logger.warning(f"Unsupported bit depth: {params.sampwidth}")
                        return audio_data
                
                    
                    # Write normalized audio
                    output_io = io.BytesIO()
                    with wave.open(output_io, 'wb') as wav_out:
                        wav_out.setparams(params)
                        wav_out.writeframes(normalized.tobytes())
                    
                    return output_io.getvalue()
        except Exception as e:
            logger.error(f"Error normalizing audio: {e}")
            return audio_data
