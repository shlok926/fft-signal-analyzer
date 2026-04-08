"""
Data Compression using Frequency Selection
Handles lossy compression by keeping only top frequencies
"""

import numpy as np
from typing import Dict, Any
import streamlit as st

from ..utils import logger


class CompressionEngine:
    """AI-powered data compression using Frequency Selection"""
    
    @staticmethod
    def compress_spectrum(spectrum_data: Any, compression_ratio: float = 0.5) -> Dict[str, Any]:
        """
        Compress spectral data using Frequency Selection
        Keeps only the most significant frequencies by magnitude
        
        Args:
            spectrum_data: SpectrumData object (freqs, magnitude, phase, psd)
            compression_ratio: Keep ratio (0.0-1.0)
                              0.1 = keep top 10% frequencies
                              1.0 = keep all frequencies
        
        Returns:
            Dictionary with compression results
        """
        try:
            print("\n" + "="*60)
            print("🔷 SPECTRUM COMPRESSION STARTED")
            print("="*60)
            
            n_frequencies = len(spectrum_data.magnitude)
            n_keep = max(1, int(n_frequencies * compression_ratio))
            
            print(f"Total frequencies: {n_frequencies}")
            print(f"Compression ratio: {compression_ratio*100:.0f}%")
            print(f"Frequencies to keep: {n_keep}")
            
            # Find top frequencies by magnitude
            top_indices = np.argsort(spectrum_data.magnitude)[-n_keep:]
            top_indices = np.sort(top_indices)  # Sort back to frequency order
            
            # Extract top frequencies and their data
            freqs_compressed = spectrum_data.freqs[top_indices]
            magnitude_compressed = spectrum_data.magnitude[top_indices]
            phase_compressed = spectrum_data.phase[top_indices]
            psd_compressed = spectrum_data.psd[top_indices]
            
            # Calculate metrics
            original_size = (spectrum_data.magnitude.nbytes + 
                           spectrum_data.phase.nbytes + 
                           spectrum_data.psd.nbytes)
            compressed_size = (magnitude_compressed.nbytes + 
                             phase_compressed.nbytes + 
                             psd_compressed.nbytes)
            compression_ratio_actual = 1 - (compressed_size / original_size)
            
            # Calculate reconstruction error (MSE on original grid)
            # Interpolate compressed data back to original grid
            magnitude_interp = np.interp(
                spectrum_data.freqs, 
                freqs_compressed, 
                magnitude_compressed
            )
            
            magnitude_error = ((spectrum_data.magnitude - magnitude_interp) ** 2).mean()
            psd_interp = np.interp(
                spectrum_data.freqs,
                freqs_compressed,
                psd_compressed
            )
            psd_error = ((spectrum_data.psd - psd_interp) ** 2).mean()
            mse = (magnitude_error + psd_error) / 2
            
            # Calculate SNR
            signal_power = np.mean(spectrum_data.magnitude ** 2)
            snr_db = 10 * np.log10(signal_power / max(mse, 1e-10))
            
            # Energy preservation
            original_energy = np.sum(spectrum_data.magnitude ** 2)
            compressed_energy = np.sum(magnitude_compressed ** 2)
            energy_preserved = (compressed_energy / original_energy) * 100 if original_energy > 0 else 0
            
            info = f"""
            ✅ Compression Complete:
            • Compression Level: {compression_ratio*100:.0f}%
            • Frequencies Kept: {n_keep}/{n_frequencies} ({n_keep/n_frequencies*100:.1f}%)
            • Compression Ratio: {compression_ratio_actual*100:.2f}%
            • Energy Preserved: {energy_preserved:.2f}%
            • MSE: {mse:.6f}
            • SNR: {snr_db:.2f} dB
            • Method: Frequency Selection (Top-K by magnitude)
            """
            
            print(info)
            print("="*60)
            
            return {
                'magnitude': magnitude_interp,  # Interpolated back to original grid
                'magnitude_original': magnitude_compressed,
                'phase': spectrum_data.phase,
                'psd': psd_interp,  # Interpolated
                'freqs': spectrum_data.freqs,
                'freqs_kept': freqs_compressed,
                'original_size': original_size,
                'compressed_size': compressed_size,
                'compression_ratio': compression_ratio_actual,
                'mse': mse,
                'snr_db': snr_db,
                'energy_preserved': energy_preserved,
                'n_frequencies_kept': n_keep,
                'n_frequencies_total': n_frequencies,
                'info': info
            }
            
        except Exception as e:
            print(f"❌ Compression Error: {str(e)}")
            import traceback
            traceback.print_exc()
            st.error(f"Compression Error: {str(e)}")
            return None
    
    @staticmethod
    def compress_signal(signal_data: Any, compression_ratio: float = 0.5) -> Dict[str, Any]:
        """
        Compress time-domain signal by keeping significant samples
        
        Args:
            signal_data: SignalData object
            compression_ratio: Compression level (0.0-1.0)
        
        Returns:
            Dictionary with compression results
        """
        try:
            amplitude = signal_data.amplitude
            n_samples = len(amplitude)
            n_keep = max(1, int(n_samples * compression_ratio))
            
            # Keep samples with highest magnitude
            top_indices = np.argsort(np.abs(amplitude))[-n_keep:]
            top_indices = np.sort(top_indices)
            
            # Interpolate
            time_compressed = signal_data.time[top_indices]
            amplitude_compressed = amplitude[top_indices]
            
            amplitude_interp = np.interp(signal_data.time, time_compressed, amplitude_compressed)
            
            mse = ((amplitude - amplitude_interp) ** 2).mean()
            signal_power = np.mean(amplitude ** 2)
            snr_db = 10 * np.log10(signal_power / max(mse, 1e-10))
            
            original_size = amplitude.nbytes
            compressed_size = amplitude_compressed.nbytes + time_compressed.nbytes
            compression_ratio_actual = 1 - (compressed_size / original_size)
            
            return {
                'amplitude': amplitude_interp,
                'time': signal_data.time,
                'fs': signal_data.fs,
                'original_size': original_size,
                'compressed_size': compressed_size,
                'compression_ratio': compression_ratio_actual,
                'mse': mse,
                'snr_db': snr_db,
                'n_samples_kept': n_keep,
                'n_samples_total': n_samples
            }
            
        except Exception as e:
            logger.error(f"Signal compression error: {str(e)}")
            return None
