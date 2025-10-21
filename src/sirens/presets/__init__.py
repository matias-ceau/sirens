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
        "description": "French Police two-tone siren",
    },
    # Firefighter two-tone siren (Sapeurs-Pompiers)
    "firefighter": {
        "freqs": (370, 470),  # Two-tone frequencies in Hz
        "tone_duration": 0.7,  # Slower alternation rate
        "attack": 0.1,  # Attack time in seconds
        "decay": 0.1,  # Decay time in seconds
        "volume": 1.0,  # Relative volume (0-1)
        "max_db": 112,  # Approximate max dB level
        "description": "French Firefighter (Sapeurs-Pompiers) two-tone siren",
    },
    # SAMU/Ambulance two-tone siren
    "samu": {
        "freqs": (435, 651),  # Two-tone frequencies in Hz
        "tone_duration": 0.3,  # Faster alternation rate
        "attack": 0.04,  # Attack time in seconds
        "decay": 0.04,  # Decay time in seconds
        "volume": 0.85,  # Relative volume (0-1)
        "max_db": 108,  # Approximate max dB level
        "description": "French SAMU/Ambulance two-tone siren",
    },
    # "Hi-Lo" European-style sweep siren
    "hi_lo": {
        "freqs": (440, 660),  # Hi-Lo frequencies in Hz
        "tone_duration": 0.5,  # Alternation rate
        "attack": 0.05,  # Attack time in seconds
        "decay": 0.05,  # Decay time in seconds
        "volume": 0.9,  # Relative volume (0-1)
        "max_db": 110,  # Approximate max dB level
        "description": "European-style Hi-Lo sweep siren",
    },
}


def validate_siren_preset(preset):
    """Validate a siren preset configuration.
    
    Args:
        preset: Dictionary containing siren configuration
        
    Returns:
        tuple: (is_valid, error_message)
    """
    required_fields = ["freqs", "tone_duration", "attack", "decay", "volume", "max_db"]
    
    for field in required_fields:
        if field not in preset:
            return False, f"Missing required field: {field}"
    
    # Validate freqs
    if not isinstance(preset["freqs"], (tuple, list)) or len(preset["freqs"]) != 2:
        return False, "freqs must be a tuple or list of 2 frequencies"
    
    if not all(isinstance(f, (int, float)) and f > 0 for f in preset["freqs"]):
        return False, "Frequencies must be positive numbers"
    
    # Validate numeric fields
    numeric_fields = ["tone_duration", "attack", "decay", "volume", "max_db"]
    for field in numeric_fields:
        if not isinstance(preset[field], (int, float)) or preset[field] < 0:
            return False, f"{field} must be a non-negative number"
    
    # Validate volume range
    if preset["volume"] > 1.0:
        return False, "volume must be between 0 and 1"
    
    return True, None


def register_custom_siren(name, preset):
    """Register a custom siren preset.
    
    Args:
        name: Name for the custom siren
        preset: Dictionary containing siren configuration with keys:
            - freqs: Tuple of two frequencies in Hz (freq1, freq2)
            - tone_duration: Duration of each tone in seconds
            - attack: Attack time in seconds
            - decay: Decay time in seconds
            - volume: Volume level (0.0-1.0)
            - max_db: Maximum dB level at source
            - description: Optional description of the siren
            
    Raises:
        ValueError: If preset is invalid
    """
    is_valid, error = validate_siren_preset(preset)
    if not is_valid:
        raise ValueError(f"Invalid siren preset: {error}")
    
    # Add description if not present
    if "description" not in preset:
        preset = preset.copy()
        preset["description"] = f"Custom {name} siren"
    
    PRESETS[name] = preset


def get_available_sirens():
    """Get a list of all available siren types.
    
    Returns:
        dict: Dictionary mapping siren names to their descriptions
    """
    return {
        name: preset.get("description", f"{name} siren")
        for name, preset in PRESETS.items()
    }
