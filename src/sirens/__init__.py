"""French emergency vehicle siren simulator.

Generate, play, and manipulate realistic siren sounds.
"""

__version__ = "0.1.0"

import math
import os
import random
import struct
import sys
import wave
from datetime import datetime

import numpy as np


class Siren:
    # Updated presets based on more accurate frequency information for French emergency vehicles
    # These values are approximations based on available research
    presets = {
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

    def __init__(
        self,
        name="police",
        total_duration=10,
        night_mode=False,
        traffic_density="medium",
        distance=10,
    ):
        """
        Initialize a siren simulation

        Parameters:
        - name: Type of siren (police, firefighter, samu, hi_lo)
        - total_duration: Total duration in seconds
        - night_mode: If True, reduces volume (simulating night regulations)
        - traffic_density: "light", "medium", or "heavy" to simulate different usage patterns
        - distance: Simulated distance from the listener in meters
        """
        self.p = self.presets.get(name, self.presets["police"]).copy()
        self.freq1, self.freq2 = self.p["freqs"]
        self.tone_duration = self.p["tone_duration"]
        self.attack = self.p["attack"]
        self.decay = self.p["decay"]
        self.total_duration = total_duration
        self.sample_rate = 44100
        self.night_mode = night_mode
        self.traffic_density = traffic_density
        self.distance = distance

        # Apply night mode volume reduction (Brussels standard limits to 90dB at night)
        if night_mode:
            self.p["volume"] *= 0.5  # Significant volume reduction at night

        # Adjust volume based on distance (inverse square law approximation)
        self.p["volume"] *= min(1.0, (10 / max(1, distance)) ** 2)

        # Adjust siren pattern based on traffic density
        if traffic_density == "heavy":
            # More continuous siren in heavy traffic
            self.duty_cycle = 0.9  # 90% on, 10% off
            self.burst_size = 6  # Longer bursts
        elif traffic_density == "light":
            # More intermittent siren in light traffic
            self.duty_cycle = 0.6  # 60% on, 40% off
            self.burst_size = 2  # Shorter bursts
        else:  # medium
            # Standard pattern
            self.duty_cycle = 0.8  # 80% on, 20% off
            self.burst_size = 4  # Medium bursts

        # Calculate how many complete cycles we need
        self.cycles = int(total_duration / (2 * self.tone_duration) * self.duty_cycle)

        # Generate the samples
        self.samples = self._generate()

    def _envelope(self, samples, attack, decay):
        """Apply an attack/decay envelope to a sample array"""
        attack_samples = int(attack * self.sample_rate)
        decay_samples = int(decay * self.sample_rate)
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

    def _sine(self, freq, duration):
        """Generate a sine wave with the specified frequency and duration"""
        n = int(self.sample_rate * duration)
        base = [math.sin(2 * math.pi * freq * t / self.sample_rate) for t in range(n)]

        # Add slight harmonic distortion for realism
        harmonic_factor = 0.15
        harmonic = [
            harmonic_factor * math.sin(4 * math.pi * freq * t / self.sample_rate)
            for t in range(n)
        ]

        combined = [base[i] + harmonic[i] for i in range(n)]

        # Normalize to prevent clipping
        max_val = max(abs(min(combined)), abs(max(combined)))
        normalized = [s / max_val for s in combined]

        # Apply attack/decay envelope
        return self._envelope(normalized, self.attack, self.decay)

    def _generate(self):
        """Generate the complete siren signal"""
        signal = []

        # Add slight variations to make it more realistic
        freq1_var = self.freq1 * 0.01  # 1% variation
        freq2_var = self.freq2 * 0.01  # 1% variation

        # Generate in bursts with pauses to simulate realistic usage patterns
        remaining_cycles = self.cycles
        while remaining_cycles > 0:
            # Determine burst size (how many tone pairs to generate before a pause)
            burst = min(remaining_cycles, self.burst_size)
            remaining_cycles -= burst

            # Generate the burst
            for _ in range(burst):
                # Add slight randomness to frequencies for realism
                f1 = self.freq1 + random.uniform(-freq1_var, freq1_var)
                f2 = self.freq2 + random.uniform(-freq2_var, freq2_var)

                signal += self._sine(f1, self.tone_duration)
                signal += self._sine(f2, self.tone_duration)

            # Add a pause if not the last burst
            if remaining_cycles > 0:
                pause_duration = (
                    self.tone_duration * 2 * (1 - self.duty_cycle) / (self.duty_cycle)
                )
                signal += [0] * int(pause_duration * self.sample_rate)

        # Apply overall volume
        return [s * self.p["volume"] for s in signal]

    def get_info(self):
        """Return information about this siren configuration"""
        info = {
            "frequencies": self.p["freqs"],
            "tone_duration": self.tone_duration,
            "night_mode": self.night_mode,
            "traffic_density": self.traffic_density,
            "distance": self.distance,
            "max_db_at_source": self.p["max_db"],
            "estimated_db": self._estimate_db(),
        }
        return info

    def _estimate_db(self):
        """Estimate the actual dB level based on distance and night mode"""
        # This is a simplified model for estimation purposes
        if self.distance <= 0:
            return self.p["max_db"]

        # Basic inverse square law for sound propagation
        db_reduction = 20 * math.log10(self.distance)
        estimated_db = self.p["max_db"] - db_reduction

        # Additional reduction for night mode
        if self.night_mode:
            estimated_db = min(estimated_db, 90)  # Brussels standard night limit

        return round(estimated_db, 1)

    def write(self, filename=None):
        """Write the siren audio to a WAV file"""
        if filename is None:
            # Generate a default filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"siren_{timestamp}.wav"

        with wave.open(filename, "w") as wf:
            wf.setnchannels(1)  # Mono
            wf.setsampwidth(2)  # 16-bit
            wf.setframerate(self.sample_rate)

            # Write each sample, scaling to 16-bit range
            for s in self.samples:
                wf.writeframes(struct.pack("h", int(s * 32767)))

        return filename

    def play(self):
        """Play the siren audio"""
        tmp_file = self.write("_tmp_siren.wav")

        # Determine which command to use based on platform
        if sys.platform == "darwin":  # macOS
            os.system(f"afplay {tmp_file}")
        elif sys.platform == "linux" or sys.platform == "linux2":
            os.system(f"aplay {tmp_file}")
        elif sys.platform == "win32":
            os.system(f"start {tmp_file}")
        else:
            print(f"Audio file saved to {tmp_file} but couldn't play automatically.")


def main():
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
    if siren_type not in Siren.presets:
        print(f"Unknown siren type: {siren_type}")
        print(f"Available types: {', '.join(Siren.presets.keys())}")
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


if __name__ == "__main__":
    main()
