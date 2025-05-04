"""Command-line interface for the sirens package."""

import sys
from .core import Siren
from .presets import PRESETS


def main():
    """Process command line arguments and execute sirens functionality."""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  sirens write <siren_type> [options]")
        print("  sirens info <siren_type> [options]")
        print("\nSiren Types:")
        print("  police       - French Police two-tone")
        print("  firefighter  - French Firefighter (Sapeurs-Pompiers) two-tone")
        print("  samu         - French SAMU/Ambulance two-tone")
        print("  hi_lo        - European-style Hi-Lo sweep")
        print("\nOptions:")
        print("  --duration <seconds>        - Duration in seconds (default: 10)")
        print("  --night                     - Enable night mode (reduced volume)")
        print("  --traffic <light|medium|heavy> - Traffic density (default: medium)")
        print(
            "  --distance <meters>         - Distance from listener in meters (default: 10)"
        )
        print("  --outfile <filename>        - Output filename (write mode only)")
        return

    command = sys.argv[1]

    if len(sys.argv) < 3:
        print("Error: Siren type required")
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
