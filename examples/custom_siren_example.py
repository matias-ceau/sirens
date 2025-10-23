#!/usr/bin/env python3
"""Example script demonstrating how to create and use custom sirens.

This example shows:
1. How to list available sirens
2. How to register a custom siren
3. How to generate audio with custom sirens
4. How to use the API programmatically
"""

import sys
sys.path.insert(0, "../src")

from sirens import Siren, register_custom_siren, get_available_sirens


def main():
    print("=== Sirens Package - Custom Siren Example ===\n")
    
    # 1. List available sirens (French ones are pre-registered)
    print("1. Available sirens before adding custom ones:")
    available = get_available_sirens()
    for name, description in available.items():
        print(f"   - {name}: {description}")
    print()
    
    # 2. Create and register a custom siren
    print("2. Registering a custom siren...")
    
    # Example: US-style wail siren
    us_wail_preset = {
        "freqs": (650, 1200),        # Higher frequencies for US sirens
        "tone_duration": 0.8,         # Slower sweep
        "attack": 0.1,
        "decay": 0.1,
        "volume": 0.95,
        "max_db": 118,
        "description": "US-style wail siren (custom example)"
    }
    
    try:
        register_custom_siren("us_wail", us_wail_preset)
        print("   ✓ Successfully registered 'us_wail' siren")
    except ValueError as e:
        print(f"   ✗ Error: {e}")
        return
    
    # Example: Low-frequency industrial warning
    industrial_preset = {
        "freqs": (200, 300),          # Very low frequencies
        "tone_duration": 1.0,          # Slow alternation
        "attack": 0.2,
        "decay": 0.2,
        "volume": 0.7,
        "max_db": 105,
        "description": "Industrial warning siren (custom example)"
    }
    
    register_custom_siren("industrial", industrial_preset)
    print("   ✓ Successfully registered 'industrial' siren")
    print()
    
    # 3. List sirens again to see custom ones
    print("3. Available sirens after adding custom ones:")
    available = get_available_sirens()
    for name, description in available.items():
        print(f"   - {name}: {description}")
    print()
    
    # 4. Generate audio files with different sirens
    print("4. Generating audio files...")
    
    # French police siren (pre-registered)
    print("   - Generating French police siren...")
    police_siren = Siren(name="police", total_duration=3)
    police_file = police_siren.write("example_police_3s.wav")
    print(f"     Saved to: {police_file}")
    
    # Custom US wail siren
    print("   - Generating custom US wail siren...")
    us_siren = Siren(name="us_wail", total_duration=3)
    us_file = us_siren.write("example_us_wail_3s.wav")
    print(f"     Saved to: {us_file}")
    
    # Custom industrial siren with night mode
    print("   - Generating custom industrial siren (night mode)...")
    industrial_siren = Siren(
        name="industrial", 
        total_duration=3,
        night_mode=True,
        distance=30
    )
    industrial_file = industrial_siren.write("example_industrial_3s.wav")
    print(f"     Saved to: {industrial_file}")
    print()
    
    # 5. Show detailed information
    print("5. Detailed information about custom 'us_wail' siren:")
    info = us_siren.get_info()
    print(f"   Frequencies: {info['frequencies'][0]} Hz / {info['frequencies'][1]} Hz")
    print(f"   Tone duration: {info['tone_duration']} seconds")
    print(f"   Max dB at source: {info['max_db_at_source']} dB")
    print(f"   Estimated dB at listener: {info['estimated_db']} dB")
    print()
    
    # 6. Example of invalid preset (will fail validation)
    print("6. Attempting to register an invalid siren (missing required fields)...")
    invalid_preset = {
        "freqs": (400, 500),
        # Missing other required fields
    }
    
    try:
        register_custom_siren("invalid", invalid_preset)
        print("   ✗ Should have failed validation!")
    except ValueError as e:
        print(f"   ✓ Correctly rejected: {e}")
    print()
    
    print("=== Example Complete ===")
    print("\nYou can also use the CLI to work with custom sirens after registering them in code:")
    print("  sirens list")
    print("  sirens info us_wail")
    print("  sirens write us_wail --duration 10")


if __name__ == "__main__":
    main()
