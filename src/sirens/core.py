"""Core Siren class implementation."""

from datetime import datetime

from .presets import PRESETS
from .generators import generate_siren_signal
from .playback import write_wav, play_audio
from .utils import estimate_db


class Siren:
    """Create and manipulate emergency vehicle siren sounds."""

    def __init__(
        self,
        name="police",
        total_duration=10,
        night_mode=False,
        traffic_density="medium",
        distance=10,
    ):
        """
        Initialize a siren simulation.

        Parameters:
            name: Type of siren (police, firefighter, samu, hi_lo)
            total_duration: Total duration in seconds
            night_mode: If True, reduces volume (simulating night regulations)
            traffic_density: "light", "medium", or "heavy" to simulate different usage patterns
            distance: Simulated distance from the listener in meters
        """
        self.presets = PRESETS
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

    def _generate(self):
        """Generate the complete siren signal."""
        return generate_siren_signal(
            freq1=self.freq1,
            freq2=self.freq2,
            tone_duration=self.tone_duration,
            attack=self.attack,
            decay=self.decay,
            cycles=self.cycles,
            duty_cycle=self.duty_cycle,
            burst_size=self.burst_size,
            sample_rate=self.sample_rate,
            volume=self.p["volume"],
        )

    def _estimate_db(self):
        """Estimate the actual dB level based on distance and night mode."""
        return estimate_db(self.p["max_db"], self.distance, self.night_mode)

    def get_info(self):
        """Return information about this siren configuration."""
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

    def write(self, filename=None):
        """Write the siren audio to a WAV file."""
        if filename is None:
            # Generate a default filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"siren_{timestamp}.wav"

        return write_wav(self.samples, filename, self.sample_rate)

    def play(self):
        """Play the siren audio."""
        tmp_file = self.write("_tmp_siren.wav")
        return play_audio(tmp_file)
