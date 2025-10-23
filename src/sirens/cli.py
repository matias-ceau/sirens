"""Command-line interface for the sirens package."""

import sys
from .core import Siren
from .presets import PRESETS, get_available_sirens


def main():
    """Process command line arguments and execute sirens functionality."""
    if len(sys.argv) < 2:
        print_usage()
        return

    command = sys.argv[1]

    # Handle list command without requiring a siren type
    if command == "list":
        list_sirens()
        return

    if len(sys.argv) < 3:
        print("Error: Siren type required")
        print_usage()
        return

    siren_type = sys.argv[2]

    # Parse optional arguments
    duration = 10
    night_mode = False
    traffic_density = "medium"
    distance = 10
    outfile = None

    i = 3
    while i < len(sys.argv):
        if sys.argv[i] == "--duration" and i + 1 < len(sys.argv):
            try:
                duration = float(sys.argv[i + 1])
                i += 2
            except ValueError:
                print(f"Invalid duration: {sys.argv[i + 1]}")
                return
        elif sys.argv[i] == "--night":
            night_mode = True
            i += 1
        elif sys.argv[i] == "--traffic" and i + 1 < len(sys.argv):
            traffic_density = sys.argv[i + 1]
            if traffic_density not in ["light", "medium", "heavy"]:
                print(f"Invalid traffic density: {traffic_density}")
                return
            i += 2
        elif sys.argv[i] == "--distance" and i + 1 < len(sys.argv):
            try:
                distance = float(sys.argv[i + 1])
                i += 2
            except ValueError:
                print(f"Invalid distance: {sys.argv[i + 1]}")
                return
        elif sys.argv[i] == "--outfile" and i + 1 < len(sys.argv):
            outfile = sys.argv[i + 1]
            i += 2
        else:
            print(f"Unknown option: {sys.argv[i]}")
            return

    # Verify siren type
    if siren_type not in PRESETS:
        print(f"Unknown siren type: {siren_type}")
        print(f"Available types: {', '.join(PRESETS.keys())}")
        print("\nUse 'sirens list' to see detailed information about available sirens.")
        return

    # Create siren
    siren = Siren(
        name=siren_type,
        total_duration=duration,
        night_mode=night_mode,
        traffic_density=traffic_density,
        distance=distance,
    )

    # Execute command
    if command == "play":
        print(f"Playing {siren_type} siren...")
        print(f"Estimated dB level: {siren._estimate_db()} dB")
        siren.play()
    elif command == "write":
        if outfile is None:
            outfile = f"{siren_type}_{int(duration)}s.wav"
        filename = siren.write(outfile)
        print(f"Wrote {filename}")
        print(f"Estimated dB level: {siren._estimate_db()} dB")
    elif command == "info":
        info = siren.get_info()
        print("\nSiren Information:")
        print(f"Type: {siren_type}")
        print(
            f"Frequencies: {info['frequencies'][0]} Hz and {info['frequencies'][1]} Hz"
        )
        print(f"Tone duration: {info['tone_duration']} seconds")
        print(f"Night mode: {'Enabled' if info['night_mode'] else 'Disabled'}")
        print(f"Traffic density: {info['traffic_density']}")
        print(f"Distance from listener: {info['distance']} meters")
        print(f"Maximum dB at source: {info['max_db_at_source']} dB")
        print(f"Estimated dB at listener: {info['estimated_db']} dB\n")
    else:
        print(f"Unknown command: {command}")
        print_usage()


def list_sirens():
    """List all available siren types with descriptions."""
    available = get_available_sirens()
    print("\n=== Available Siren Types ===\n")
    
    # Separate French sirens from others
    french_sirens = ["police", "firefighter", "samu"]
    other_sirens = [name for name in available.keys() if name not in french_sirens]
    
    print("French Emergency Vehicle Sirens:")
    for name in french_sirens:
        if name in available:
            preset = PRESETS[name]
            freqs = preset["freqs"]
            print(f"  {name:15s} - {available[name]}")
            print(f"                    Frequencies: {freqs[0]} Hz / {freqs[1]} Hz")
    
    if other_sirens:
        print("\nOther Sirens:")
        for name in other_sirens:
            preset = PRESETS[name]
            freqs = preset["freqs"]
            print(f"  {name:15s} - {available[name]}")
            print(f"                    Frequencies: {freqs[0]} Hz / {freqs[1]} Hz")
    
    print("\nUse 'sirens info <siren_type>' for detailed information about a specific siren.")
    print()


def print_usage():
    """Print usage information."""
    print("Usage:")
    print("  sirens list                           - List all available siren types")
    print("  sirens info <siren_type> [options]    - Show detailed siren information")
    print("  sirens write <siren_type> [options]   - Generate and save siren audio")
    print("  sirens play <siren_type> [options]    - Generate and play siren audio")
    print("\nFrench Siren Types:")
    print("  police       - French Police two-tone")
    print("  firefighter  - French Firefighter (Sapeurs-Pompiers) two-tone")
    print("  samu         - French SAMU/Ambulance two-tone")
    print("\nOther Siren Types:")
    print("  hi_lo        - European-style Hi-Lo sweep")
    print("\nOptions:")
    print("  --duration <seconds>                  - Duration in seconds (default: 10)")
    print("  --night                               - Enable night mode (reduced volume)")
    print("  --traffic <light|medium|heavy>        - Traffic density (default: medium)")
    print("  --distance <meters>                   - Distance from listener in meters (default: 10)")
    print("  --outfile <filename>                  - Output filename (write mode only)")
    print("\nExamples:")
    print("  sirens list")
    print("  sirens info police")
    print("  sirens write police --duration 5 --outfile my_siren.wav")
    print("  sirens play samu --night --distance 50")
