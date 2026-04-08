"""Signal loading from external files."""

from pathlib import Path

import numpy as np

from ..models import SignalData
from ..utils import logger, validate_signal_file, validate_csv_format


class SignalLoader:
    """Load signals from various file formats."""

    @staticmethod
    def load_csv(file_path: str, fs: float = 1000.0) -> SignalData:
        """Load signal from CSV file.
        
        CSV should have either:
        - 1 column: amplitude values (time computed from fs)
        - 2 columns: [time, amplitude]
        
        Args:
            file_path: Path to CSV file.
            fs: Sampling frequency in Hz (used if CSV has only 1 column).
            
        Returns:
            SignalData object.
            
        Raises:
            ValueError: If file format is invalid.
        """
        import pandas as pd

        # Validate file
        is_valid, error_msg = validate_signal_file(file_path)
        if not is_valid:
            raise ValueError(error_msg)

        # Validate CSV format
        is_valid, error_msg = validate_csv_format(file_path)
        if not is_valid:
            raise ValueError(error_msg)

        try:
            df = pd.read_csv(file_path)

            if df.shape[1] == 1:
                # Single column: amplitude only
                amplitude = df.iloc[:, 0].values.astype(np.float64)
                num_samples = len(amplitude)
                time = np.linspace(0, (num_samples - 1) / fs, num_samples)
                logger.info(f"Loaded CSV with 1 column. Inferred fs={fs} Hz.")
            elif df.shape[1] == 2:
                # Two columns: [time, amplitude]
                time = df.iloc[:, 0].values.astype(np.float64)
                amplitude = df.iloc[:, 1].values.astype(np.float64)
                # Infer actual fs from time axis
                if len(time) > 1:
                    fs = 1.0 / (time[1] - time[0])
                logger.info(f"Loaded CSV with 2 columns. Inferred fs={fs} Hz.")

            # Center on mean (remove DC)
            amplitude = amplitude - np.mean(amplitude)

            return SignalData(
                time=time,
                amplitude=amplitude,
                fs=fs,
                label=Path(file_path).stem,
                source="csv",
            )

        except Exception as e:
            logger.error(f"Error loading CSV: {str(e)}")
            raise ValueError(f"Failed to load CSV: {str(e)}")

    @staticmethod
    def load_wav(file_path: str) -> SignalData:
        """Load signal from WAV file.
        
        Args:
            file_path: Path to WAV file.
            
        Returns:
            SignalData object.
            
        Raises:
            ValueError: If file format is invalid.
        """
        import scipy.io.wavfile as wavfile

        # Validate file
        is_valid, error_msg = validate_signal_file(file_path)
        if not is_valid:
            raise ValueError(error_msg)

        try:
            fs_wav, audio_data = wavfile.read(file_path)

            # Handle stereo → mono conversion
            if len(audio_data.shape) > 1:
                # Stereo: average channels
                audio_data = np.mean(audio_data, axis=1)

            # Convert to float64 and normalize
            amplitude = audio_data.astype(np.float64)

            # Normalize to [-1, 1]
            if np.max(np.abs(amplitude)) > 0:
                amplitude = amplitude / np.max(np.abs(amplitude))

            # Remove DC offset
            amplitude = amplitude - np.mean(amplitude)

            # Generate time axis
            num_samples = len(amplitude)
            time = np.linspace(0, (num_samples - 1) / fs_wav, num_samples)

            logger.info(
                f"Loaded WAV file: fs={fs_wav} Hz, samples={num_samples}, "
                f"duration={time[-1]:.2f}s"
            )

            return SignalData(
                time=time,
                amplitude=amplitude,
                fs=float(fs_wav),
                label=Path(file_path).stem,
                source="wav",
            )

        except Exception as e:
            logger.error(f"Error loading WAV: {str(e)}")
            raise ValueError(f"Failed to load WAV: {str(e)}")

    @staticmethod
    def load_npy(file_path: str, fs: float = 1000.0) -> SignalData:
        """Load signal from NumPy .npy file.
        
        Expected: 1D or 2D array where last dimension is samples.
        
        Args:
            file_path: Path to .npy file.
            fs: Sampling frequency in Hz.
            
        Returns:
            SignalData object.
            
        Raises:
            ValueError: If file format is invalid.
        """
        # Validate file
        is_valid, error_msg = validate_signal_file(file_path)
        if not is_valid:
            raise ValueError(error_msg)

        try:
            data = np.load(file_path)

            if data.ndim == 1:
                amplitude = data.astype(np.float64)
            elif data.ndim == 2:
                # Take first row or flatten
                amplitude = data.flatten().astype(np.float64)
            else:
                raise ValueError(
                    f"Expected 1D or 2D array, got {data.ndim}D"
                )

            # Remove DC
            amplitude = amplitude - np.mean(amplitude)

            # Generate time axis
            num_samples = len(amplitude)
            time = np.linspace(0, (num_samples - 1) / fs, num_samples)

            logger.info(
                f"Loaded NPY file: fs={fs} Hz, samples={num_samples}, "
                f"duration={time[-1]:.2f}s"
            )

            return SignalData(
                time=time,
                amplitude=amplitude,
                fs=fs,
                label=Path(file_path).stem,
                source="npy",
            )

        except Exception as e:
            logger.error(f"Error loading NPY: {str(e)}")
            raise ValueError(f"Failed to load NPY: {str(e)}")

    @staticmethod
    def validate(signal_data: SignalData) -> bool:
        """Validate loaded signal data.
        
        Args:
            signal_data: SignalData object to validate.
            
        Returns:
            True if valid, raises ValueError otherwise.
        """
        if len(signal_data.time) < 4:
            msg = "Signal too short. Minimum 4 samples required."
            logger.error(msg)
            raise ValueError(msg)

        if signal_data.fs <= 0:
            msg = "Invalid sampling frequency"
            logger.error(msg)
            raise ValueError(msg)

        if np.any(np.isnan(signal_data.amplitude)):
            msg = "Signal contains NaN values"
            logger.error(msg)
            raise ValueError(msg)

        if np.any(np.isinf(signal_data.amplitude)):
            msg = "Signal contains infinite values"
            logger.error(msg)
            raise ValueError(msg)

        if np.allclose(signal_data.amplitude, 0):
            logger.warning("Signal is all-zero or near-zero")

        logger.info(f"Signal validated: {signal_data.label} ({signal_data.source})")
        return True
