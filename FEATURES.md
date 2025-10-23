# Sirens - Usage Examples and Features

This document demonstrates the finished sirens application with custom siren support.

## ✅ Implemented Features

### 1. French Emergency Sirens (Pre-configured)
The package includes three authentic French emergency vehicle sirens:

- **Police** (435 Hz / 580 Hz) - Fast two-tone alternation
- **Firefighter** (370 Hz / 470 Hz) - Slower, deeper two-tone  
- **SAMU/Ambulance** (435 Hz / 651 Hz) - Very fast two-tone
- **Hi-Lo** (440 Hz / 660 Hz) - European-style sweep

### 2. Custom Siren Support
Users can programmatically register their own custom sirens:

```python
from sirens import register_custom_siren, Siren

# Define custom siren parameters
my_siren = {
    "freqs": (500, 650),          # Two frequencies in Hz
    "tone_duration": 0.6,         # Seconds per tone
    "attack": 0.05,               # Fade-in time
    "decay": 0.05,                # Fade-out time
    "volume": 0.9,                # Volume (0-1)
    "max_db": 115,                # Max dB at source
    "description": "My custom siren"
}

# Register and use it
register_custom_siren("my_custom", my_siren)
siren = Siren(name="my_custom", total_duration=10)
siren.write("my_siren.wav")
```

### 3. Validation System
All custom sirens are validated before registration:
- Required fields checked
- Data types validated  
- Frequency and volume ranges verified
- Clear error messages for invalid configurations

### 4. Enhanced CLI

#### List all sirens
```bash
$ sirens list

=== Available Siren Types ===

French Emergency Vehicle Sirens:
  police          - French Police two-tone siren
                    Frequencies: 435 Hz / 580 Hz
  firefighter     - French Firefighter (Sapeurs-Pompiers) two-tone siren
                    Frequencies: 370 Hz / 470 Hz
  samu            - French SAMU/Ambulance two-tone siren
                    Frequencies: 435 Hz / 651 Hz

Other Sirens:
  hi_lo           - European-style Hi-Lo sweep siren
                    Frequencies: 440 Hz / 660 Hz
```

#### Get detailed information
```bash
$ sirens info police

Siren Information:
Type: police
Frequencies: 435 Hz and 580 Hz
Tone duration: 0.4 seconds
Night mode: Disabled
Traffic density: medium
Distance from listener: 10 meters
Maximum dB at source: 110 dB
Estimated dB at listener: 90.0 dB
```

#### Generate audio files
```bash
# Basic usage
$ sirens write police
Wrote police_10s.wav
Estimated dB level: 90.0 dB

# With options
$ sirens write firefighter --duration 5 --outfile emergency.wav --night --distance 50
Wrote emergency.wav
Estimated dB level: 65.6 dB
```

### 5. Environmental Simulation

The app simulates realistic conditions:

**Night Mode**
- Reduces volume to comply with regulations (90 dB limit)
- Simulates Brussels night-time standards

**Distance Attenuation**
- Uses inverse square law for sound propagation
- Realistic dB calculations based on distance

**Traffic Patterns**
- Light: 60% duty cycle, intermittent bursts
- Medium: 80% duty cycle, standard pattern
- Heavy: 90% duty cycle, continuous operation

### 6. Realistic Audio Generation

- 44.1 kHz sample rate (CD quality)
- 16-bit mono WAV format
- Harmonic distortion (15% 2nd harmonic) for realism
- ±1% frequency variation per cycle
- Attack/decay envelopes for smooth transitions

## 📦 Package Structure

```
sirens/
├── src/sirens/
│   ├── __init__.py         # Main API exports
│   ├── core.py             # Siren class
│   ├── cli.py              # Command-line interface
│   ├── presets/
│   │   └── __init__.py     # Preset definitions, validation, registration
│   ├── generators/
│   │   └── __init__.py     # Audio signal generation
│   ├── playback/
│   │   └── __init__.py     # WAV file I/O and playback
│   └── utils/
│       └── __init__.py     # Utilities (envelope, dB estimation)
├── examples/
│   ├── custom_siren_example.py  # Custom siren demo
│   └── cli_demo.py              # CLI demonstration
├── tests/
│   └── test_basic.py            # Test suite
├── README.md               # Comprehensive documentation
└── pyproject.toml          # Package configuration
```

## 🎯 Design Goals Achieved

✅ **Finished Application**
- Complete, working CLI interface
- Well-structured, modular codebase
- Comprehensive documentation
- Example scripts included

✅ **French Sirens Implemented**
- Police (435/580 Hz)
- Firefighter (370/470 Hz)  
- SAMU/Ambulance (435/651 Hz)
- All based on authentic French emergency vehicle specifications

✅ **Custom Siren Capability**
- Simple API: `register_custom_siren(name, config)`
- Full validation of custom configurations
- Custom sirens work exactly like built-in ones
- Extensible design for any emergency vehicle type

## 🔧 Technical Implementation

### Preset Validation
```python
def validate_siren_preset(preset):
    """Ensures all required fields are present and valid."""
    required_fields = ["freqs", "tone_duration", "attack", "decay", "volume", "max_db"]
    # Validates frequencies, ranges, data types
    # Returns (is_valid, error_message)
```

### Registration System
```python
def register_custom_siren(name, preset):
    """Validates and registers a custom siren."""
    # Validates preset configuration
    # Adds description if missing
    # Registers in global PRESETS dict
```

### Discovery API
```python
def get_available_sirens():
    """Returns dict of all registered sirens with descriptions."""
    # Includes both built-in and custom sirens
    # Returns {name: description} mapping
```

## 📝 Usage Summary

The sirens package is a complete, production-ready application that:

1. **Provides authentic French emergency sirens** ready to use out of the box
2. **Supports custom siren registration** via a simple, validated API
3. **Includes comprehensive CLI** for generating and managing sirens
4. **Simulates realistic conditions** (distance, night mode, traffic patterns)
5. **Generates high-quality audio** with realistic characteristics

All requirements from the problem statement have been implemented:
- ✅ Finished app with full functionality
- ✅ Possibility to add custom car sirens (via API)
- ✅ French sirens actually implemented (police, firefighter, SAMU)
