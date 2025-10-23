# Sirens

A Python package for generating realistic French emergency vehicle siren sounds. This app supports French Police, Firefighter (Sapeurs-Pompiers), and SAMU/Ambulance sirens, with the ability to add custom siren configurations.

## Features

- **French Emergency Sirens**: Authentic two-tone sirens for Police, Firefighters, and SAMU/Ambulance
- **Custom Siren Support**: Add your own custom siren configurations programmatically
- **Realistic Sound Generation**: Includes harmonic distortion, frequency variations, and burst patterns
- **Environmental Factors**: Simulates distance attenuation and night mode regulations
- **Traffic-Aware Patterns**: Adjustable siren patterns based on traffic density
- **CLI Interface**: Easy-to-use command-line interface for generating and playing sirens

## Installation

```bash
pip install -e .
```

## French Emergency Sirens

This package includes authentic French emergency vehicle sirens:

### Police
- **Frequencies**: 435 Hz / 580 Hz
- **Pattern**: Fast two-tone alternation (0.4s per tone)
- **Max dB**: 110 dB at source
- **Usage**: French Police vehicles

### Firefighter (Sapeurs-Pompiers)
- **Frequencies**: 370 Hz / 470 Hz  
- **Pattern**: Slower two-tone alternation (0.7s per tone)
- **Max dB**: 112 dB at source
- **Usage**: French Fire Department vehicles

### SAMU (Ambulance)
- **Frequencies**: 435 Hz / 651 Hz
- **Pattern**: Very fast two-tone alternation (0.3s per tone)
- **Max dB**: 108 dB at source
- **Usage**: French emergency medical services

## Command-Line Usage

### List Available Sirens
```bash
sirens list
```

### Get Detailed Information
```bash
sirens info police
sirens info firefighter
sirens info samu
```

### Generate Audio File
```bash
# Basic usage
sirens write police

# With options
sirens write police --duration 5 --outfile my_police_siren.wav

# Night mode with distance
sirens write samu --night --distance 50 --duration 10
```

### Play Siren (requires system audio player)
```bash
sirens play police
sirens play firefighter --traffic heavy
```

### Options

- `--duration <seconds>`: Duration of the siren (default: 10)
- `--night`: Enable night mode (reduces volume to comply with regulations)
- `--traffic <light|medium|heavy>`: Traffic density affects pattern (default: medium)
- `--distance <meters>`: Simulated distance from listener (default: 10)
- `--outfile <filename>`: Output filename for write command

## Python API Usage

### Basic Usage

```python
from sirens import Siren

# Create a French police siren
siren = Siren(name="police", total_duration=10)

# Generate and save to file
siren.write("police_siren.wav")

# Get information about the siren
info = siren.get_info()
print(f"Frequencies: {info['frequencies']}")
print(f"Estimated dB: {info['estimated_db']}")
```

### With Environmental Factors

```python
from sirens import Siren

# Create a siren with night mode and distance
siren = Siren(
    name="firefighter",
    total_duration=15,
    night_mode=True,      # Reduced volume for night regulations
    traffic_density="heavy",  # More continuous pattern
    distance=50           # 50 meters away
)

siren.write("distant_firefighter.wav")
```

### Adding Custom Sirens

```python
from sirens import register_custom_siren, Siren

# Define a custom siren configuration
custom_preset = {
    "freqs": (500, 600),      # Two frequencies in Hz
    "tone_duration": 0.5,     # Duration of each tone
    "attack": 0.05,           # Attack time
    "decay": 0.05,            # Decay time
    "volume": 0.9,            # Volume (0-1)
    "max_db": 115,            # Max dB at source
    "description": "My Custom Emergency Siren"
}

# Register the custom siren
register_custom_siren("my_siren", custom_preset)

# Use it like any other siren
siren = Siren(name="my_siren", total_duration=10)
siren.write("my_custom_siren.wav")
```

### List Available Sirens Programmatically

```python
from sirens import get_available_sirens

sirens = get_available_sirens()
for name, description in sirens.items():
    print(f"{name}: {description}")
```

## Custom Siren Configuration

A custom siren preset must include these fields:

- **freqs**: Tuple of two frequencies in Hz, e.g., `(440, 550)`
- **tone_duration**: Duration of each tone in seconds, e.g., `0.5`
- **attack**: Attack time (fade-in) in seconds, e.g., `0.05`
- **decay**: Decay time (fade-out) in seconds, e.g., `0.05`
- **volume**: Volume level from 0.0 to 1.0, e.g., `0.9`
- **max_db**: Maximum dB level at source, e.g., `110`
- **description** (optional): Human-readable description

Example:
```python
{
    "freqs": (450, 600),
    "tone_duration": 0.4,
    "attack": 0.05,
    "decay": 0.05,
    "volume": 0.85,
    "max_db": 112,
    "description": "Custom two-tone siren"
}
```

## Technical Details

### Sound Generation
- Sample rate: 44,100 Hz (CD quality)
- Format: 16-bit mono WAV
- Harmonic distortion: 15% of second harmonic for realism
- Frequency variation: ±1% random variation per cycle

### Environmental Simulation
- **Distance attenuation**: Inverse square law approximation
- **Night mode**: Limits output to 90 dB (Brussels standard)
- **Traffic patterns**:
  - Light: 60% duty cycle, short bursts
  - Medium: 80% duty cycle, medium bursts  
  - Heavy: 90% duty cycle, long continuous bursts

## Requirements

- Python >= 3.12
- numpy >= 2.2.5

## Development

The package is organized into modules:
- `core.py`: Main Siren class
- `presets/`: Siren preset definitions and custom siren support
- `generators/`: Audio signal generation
- `playback/`: WAV file writing and audio playback
- `utils/`: Utility functions (envelope, dB estimation)
- `cli.py`: Command-line interface

## License

See LICENSE file for details.

## Author

Matias Ceau (matias@ceau.net)
