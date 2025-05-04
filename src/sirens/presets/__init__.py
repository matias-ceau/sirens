"""Siren preset configurations for different emergency vehicles."""

# Updated presets based on accurate frequency information for French emergency vehicles
PRESETS = {
    # Police two-tone siren (France)
    "police": {
        "freqs": (435, 580),  # Two-tone frequencies in Hz
        "tone_duration": 0.4,  # Slightly faster alternation
        "attack": 0.05,  # Attack time in seconds
        "decay": 0.05,  # Decay time in seconds
        "volume": 0.9,  # Relative volume (0-1)
        "max_db": 110,  # Approximate max dB level
    },
    # Firefighter two-tone siren (Sapeurs-Pompiers)
    "firefighter": {
        "freqs": (370, 470),  # Two-tone frequencies in Hz
        "tone_duration": 0.7,  # Slower alternation rate
        "attack": 0.1,  # Attack time in seconds
        "decay": 0.1,  # Decay time in seconds
        "volume": 1.0,  # Relative volume (0-1)
        "max_db": 112,  # Approximate max dB level
    },
    # SAMU/Ambulance two-tone siren
    "samu": {
        "freqs": (435, 651),  # Two-tone frequencies in Hz
        "tone_duration": 0.3,  # Faster alternation rate
        "attack": 0.04,  # Attack time in seconds
        "decay": 0.04,  # Decay time in seconds
        "volume": 0.85,  # Relative volume (0-1)
        "max_db": 108,  # Approximate max dB level
    },
    # "Hi-Lo" European-style sweep siren
    "hi_lo": {
        "freqs": (440, 660),  # Hi-Lo frequencies in Hz
        "tone_duration": 0.5,  # Alternation rate
        "attack": 0.05,  # Attack time in seconds
        "decay": 0.05,  # Decay time in seconds
        "volume": 0.9,  # Relative volume (0-1)
        "max_db": 110,  # Approximate max dB level
    },
}
