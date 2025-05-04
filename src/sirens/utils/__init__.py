"""Utility functions for siren processing."""

import math
import numpy as np


def envelope(samples, attack, decay, sample_rate):
    """Apply an attack/decay envelope to a sample array.

    Args:
        samples: Audio samples to process
        attack: Attack time in seconds
        decay: Decay time in seconds
        sample_rate: Audio sample rate in Hz

    Returns:
        List of processed samples with envelope applied
    """
    attack_samples = int(attack * sample_rate)
    decay_samples = int(decay * sample_rate)
    total_samples = len(samples)

    # Create envelope
    env = np.ones(total_samples)

    # Apply attack
    if attack_samples > 0:
        env[:attack_samples] = np.linspace(0, 1, attack_samples)

    # Apply decay
    if decay_samples > 0 and total_samples > decay_samples:
        env[-decay_samples:] = np.linspace(1, 0, decay_samples)

    # Apply envelope to samples
    return [samples[i] * env[i] for i in range(total_samples)]


def estimate_db(max_db_at_source, distance, night_mode=False):
    """Estimate the actual dB level based on distance and night mode.

    Args:
        max_db_at_source: Maximum dB level at the source
        distance: Distance from the source in meters
        night_mode: Whether night mode is enabled (limits to 90dB)

    Returns:
        Estimated dB level at the listener
    """
    if distance <= 0:
        return max_db_at_source

    # Basic inverse square law for sound propagation
    db_reduction = 20 * math.log10(max(1, distance))
    estimated_db = max_db_at_source - db_reduction

    # Additional reduction for night mode
    if night_mode:
        estimated_db = min(estimated_db, 90)  # Brussels standard night limit

    return round(estimated_db, 1)
