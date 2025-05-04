"""Audio signal generators for sirens."""

import math
import random
from ..utils import envelope


def generate_sine_wave(freq, duration, sample_rate, attack, decay):
    """Generate a sine wave with the specified frequency and duration.

    Args:
        freq: Frequency in Hz
        duration: Duration in seconds
        sample_rate: Sample rate in Hz
        attack: Attack time in seconds
        decay: Decay time in seconds

    Returns:
        List of audio samples
    """
    n = int(sample_rate * duration)
    base = [math.sin(2 * math.pi * freq * t / sample_rate) for t in range(n)]

    # Add slight harmonic distortion for realism
    harmonic_factor = 0.15
    harmonic = [
        harmonic_factor * math.sin(4 * math.pi * freq * t / sample_rate)
        for t in range(n)
    ]

    combined = [base[i] + harmonic[i] for i in range(n)]

    # Normalize to prevent clipping
    max_val = max(abs(min(combined)), abs(max(combined)))
    normalized = [s / max_val for s in combined]

    # Apply attack/decay envelope
    return envelope(normalized, attack, decay, sample_rate)


def generate_siren_signal(
    freq1,
    freq2,
    tone_duration,
    attack,
    decay,
    cycles,
    duty_cycle,
    burst_size,
    sample_rate,
    volume,
):
    """Generate a complete siren signal with alternating frequencies.

    Args:
        freq1: First frequency in Hz
        freq2: Second frequency in Hz
        tone_duration: Duration of each tone in seconds
        attack: Attack time in seconds
        decay: Decay time in seconds
        cycles: Number of complete tone cycles to generate
        duty_cycle: Ratio of sound to silence
        burst_size: Number of tone pairs per burst
        sample_rate: Sample rate in Hz
        volume: Output volume scaling factor

    Returns:
        List of audio samples representing the siren signal
    """
    signal = []

    # Add slight variations to make it more realistic
    freq1_var = freq1 * 0.01  # 1% variation
    freq2_var = freq2 * 0.01  # 1% variation

    # Generate in bursts with pauses to simulate realistic usage patterns
    remaining_cycles = cycles
    while remaining_cycles > 0:
        # Determine burst size (how many tone pairs to generate before a pause)
        burst = min(remaining_cycles, burst_size)
        remaining_cycles -= burst

        # Generate the burst
        for _ in range(burst):
            # Add slight randomness to frequencies for realism
            f1 = freq1 + random.uniform(-freq1_var, freq1_var)
            f2 = freq2 + random.uniform(-freq2_var, freq2_var)

            signal += generate_sine_wave(f1, tone_duration, sample_rate, attack, decay)
            signal += generate_sine_wave(f2, tone_duration, sample_rate, attack, decay)

        # Add a pause if not the last burst
        if remaining_cycles > 0:
            pause_duration = tone_duration * 2 * (1 - duty_cycle) / duty_cycle
            signal += [0] * int(pause_duration * sample_rate)

    # Apply overall volume
    return [s * volume for s in signal]
