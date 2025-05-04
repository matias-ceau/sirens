"""Audio playback functionality for siren sounds."""

import os
import struct
import sys
import wave


def write_wav(samples, filename, sample_rate=44100):
    """Write audio samples to a WAV file.

    Args:
        samples: List of audio samples
        filename: Output filename
        sample_rate: Sample rate in Hz

    Returns:
        The filename of the written WAV file
    """
    with wave.open(filename, "w") as wf:
        wf.setnchannels(1)  # Mono
        wf.setsampwidth(2)  # 16-bit
        wf.setframerate(sample_rate)

        # Write each sample, scaling to 16-bit range
        for s in samples:
            wf.writeframes(struct.pack("h", int(s * 32767)))

    return filename


def play_audio(filename):
    """Play an audio file using the system's default audio player.

    Args:
        filename: Path to the audio file to play

    Returns:
        True if playback was attempted, False if platform is unsupported
    """
    # Determine which command to use based on platform
    if sys.platform == "darwin":  # macOS
        os.system(f"afplay {filename}")
        return True
    elif sys.platform == "linux" or sys.platform == "linux2":
        os.system(f"aplay {filename}")
        return True
    elif sys.platform == "win32":
        os.system(f"start {filename}")
        return True
    else:
        print(f"Audio file saved to {filename} but couldn't play automatically.")
        return False
