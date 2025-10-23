#!/usr/bin/env python3
"""Demo script showing CLI functionality without audio playback.

This demonstrates the list and info commands.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

# Simulate command-line arguments
original_argv = sys.argv.copy()

def demo_list_command():
    """Demo the list command."""
    print("=" * 60)
    print("DEMO: sirens list")
    print("=" * 60)
    sys.argv = ["sirens", "list"]
    from sirens.cli import main
    main()
    print()


def demo_info_command(siren_type):
    """Demo the info command."""
    print("=" * 60)
    print(f"DEMO: sirens info {siren_type}")
    print("=" * 60)
    sys.argv = ["sirens", "info", siren_type]
    from sirens.cli import main
    main()
    print()


def demo_help():
    """Demo help output."""
    print("=" * 60)
    print("DEMO: sirens (no arguments - shows help)")
    print("=" * 60)
    sys.argv = ["sirens"]
    from sirens.cli import main
    main()
    print()


def main():
    """Run CLI demos."""
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "  🚨  SIRENS CLI DEMONSTRATION  🚨  ".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "═" * 58 + "╝")
    print("\n")
    
    print("This demo shows the CLI functionality of the sirens package.")
    print("French emergency sirens are pre-configured and ready to use.\n")
    input("Press Enter to continue...")
    print()
    
    # Demo 1: Help
    demo_help()
    input("Press Enter to continue...")
    print()
    
    # Demo 2: List sirens
    demo_list_command()
    input("Press Enter to continue...")
    print()
    
    # Demo 3: Info for each French siren
    for siren in ["police", "firefighter", "samu"]:
        demo_info_command(siren)
        if siren != "samu":
            input("Press Enter to continue...")
            print()
    
    print("=" * 60)
    print("DEMO COMPLETE")
    print("=" * 60)
    print("\nKey Features Demonstrated:")
    print("  ✓ French emergency sirens (Police, Firefighter, SAMU)")
    print("  ✓ Detailed siren information")
    print("  ✓ Easy-to-use CLI interface")
    print("  ✓ Ready to generate audio files")
    print("\nTo use the package:")
    print("  1. Install: pip install -e .")
    print("  2. Generate audio: sirens write police --duration 10")
    print("  3. Get info: sirens info firefighter")
    print("  4. List all: sirens list")
    print()


if __name__ == "__main__":
    try:
        main()
    finally:
        sys.argv = original_argv
