"""Peak information model for detected frequency components."""

from dataclasses import dataclass


@dataclass
class PeakInfo:
    """Represents a detected peak in the frequency spectrum.
    
    Attributes:
        frequency: Peak frequency in Hz.
        magnitude: Peak magnitude in linear scale.
        magnitude_db: Peak magnitude in dB scale.
        prominence: Peak prominence (height above baseline).
        index: Index in the frequency array.
    """

    frequency: float
    magnitude: float
    magnitude_db: float
    prominence: float
    index: int

    def __post_init__(self) -> None:
        """Validate peak data after initialization."""
        if self.frequency < 0:
            raise ValueError("Frequency must be non-negative")
        if self.magnitude < 0:
            raise ValueError("Magnitude must be non-negative")
        if self.index < 0:
            raise ValueError("Index must be non-negative")
        if self.prominence < 0:
            raise ValueError("Prominence must be non-negative")

    def __lt__(self, other: "PeakInfo") -> bool:
        """Support sorting peaks by magnitude (descending)."""
        return self.magnitude > other.magnitude

    def __repr__(self) -> str:
        """String representation of peak."""
        return (
            f"PeakInfo(freq={self.frequency:.2f}Hz, "
            f"mag={self.magnitude:.4f}, "
            f"mag_db={self.magnitude_db:.2f}dB, "
            f"prom={self.prominence:.4f})"
        )
