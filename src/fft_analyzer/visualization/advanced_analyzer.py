"""
Advanced Analysis Tools - Spectrogram, Statistics, Frequency Analysis
"""

import numpy as np
import pandas as pd
from scipy import signal
import warnings
warnings.filterwarnings('ignore')


class SpectrogramGenerator:
    """Generate spectrograms (time-frequency analysis)"""
    
    @staticmethod
    def generate_spectrogram(signal_data, window_size=256, overlap=0.75):
        """
        Generate spectrogram (STFT visualization)
        
        Args:
            signal_data: SignalData object
            window_size: FFT window size
            overlap: Overlap ratio (0.75 = 75%)
        
        Returns:
            dict with spectrogram data and metadata
        """
        try:
            signal_array = signal_data.amplitude
            fs = signal_data.fs
            
            # Calculate hop length from overlap
            hop_length = int(window_size * (1 - overlap))
            
            # Compute STFT
            f, t, Sxx = signal.spectrogram(
                signal_array,
                fs=fs,
                window='hann',
                nperseg=window_size,
                noverlap=window_size - hop_length,
                scaling='spectrum'
            )
            
            # Convert to dB scale for better visualization
            Sxx_db = 10 * np.log10(np.abs(Sxx) + 1e-10)
            
            return {
                'frequencies': f,
                'times': t,
                'magnitude': Sxx,
                'magnitude_db': Sxx_db,
                'window_size': window_size,
                'overlap': overlap,
                'info': f"✅ Spectrogram Complete: {len(t)} time steps, {len(f)} frequencies"
            }
        
        except Exception as e:
            print(f"❌ Spectrogram Error: {str(e)}")
            return None


class StatisticalAnalyzer:
    """Statistical analysis of signals"""
    
    @staticmethod
    def analyze_signal_statistics(signal_data, spectrum_data):
        """
        Compute comprehensive signal statistics
        
        Args:
            signal_data: SignalData object
            spectrum_data: SpectrumData object
        
        Returns:
            dict with statistical metrics
        """
        try:
            amplitude = signal_data.amplitude
            magnitude = spectrum_data.magnitude
            psd = spectrum_data.psd
            
            # Time-domain statistics
            rms = np.sqrt(np.mean(amplitude**2))
            peak = np.max(np.abs(amplitude))
            peak_to_peak = np.max(amplitude) - np.min(amplitude)
            crest_factor = peak / rms if rms > 0 else 0
            
            # Statistical measures
            mean = np.mean(amplitude)
            std = np.std(amplitude)
            skewness = np.mean(((amplitude - mean) / std) ** 3) if std > 0 else 0
            kurtosis = np.mean(((amplitude - mean) / std) ** 4) - 3 if std > 0 else 0
            
            # Frequency domain statistics
            freq_power = np.sum(psd)
            freq_variance = np.var(magnitude)
            dominant_freq = spectrum_data.freqs[np.argmax(magnitude)]
            
            # Energy metrics
            total_energy = np.sum(magnitude**2)
            normalized_energy = total_energy / len(magnitude) if len(magnitude) > 0 else 0
            
            # PAPR (Peak-to-Average Power Ratio)
            avg_power = np.mean(magnitude**2)
            papr = (np.max(magnitude)**2) / avg_power if avg_power > 0 else 0
            
            return {
                'time_domain': {
                    'mean': float(mean),
                    'std': float(std),
                    'rms': float(rms),
                    'peak': float(peak),
                    'peak_to_peak': float(peak_to_peak),
                    'crest_factor': float(crest_factor),
                    'skewness': float(skewness),
                    'kurtosis': float(kurtosis),
                },
                'frequency_domain': {
                    'total_power': float(freq_power),
                    'variance': float(freq_variance),
                    'dominant_frequency': float(dominant_freq),
                    'energy': float(normalized_energy),
                    'papr': float(papr),
                },
                'normalized': {
                    'crest_factor_norm': min(float(crest_factor) / 3.0, 1.0),  # Normalized (3 is typical max)
                    'skewness_norm': min(abs(float(skewness)) / 2.0, 1.0),
                    'kurtosis_norm': min(float(kurtosis) / 5.0, 1.0),
                },
                'info': "✅ Statistical Analysis Complete"
            }
        
        except Exception as e:
            print(f"❌ Statistics Error: {str(e)}")
            return None


class FrequencyBandAnalyzer:
    """Analyze specific frequency bands"""
    
    @staticmethod
    def extract_frequency_band(spectrum_data, freq_low, freq_high):
        """
        Extract and analyze a specific frequency band
        
        Args:
            spectrum_data: SpectrumData object
            freq_low: Low frequency (Hz)
            freq_high: High frequency (Hz)
        
        Returns:
            dict with band analysis
        """
        try:
            freqs = spectrum_data.freqs
            magnitude = spectrum_data.magnitude
            psd = spectrum_data.psd
            
            # Find indices within frequency range
            mask = (freqs >= freq_low) & (freqs <= freq_high)
            band_freqs = freqs[mask]
            band_magnitude = magnitude[mask]
            band_psd = psd[mask]
            
            if len(band_magnitude) == 0:
                return None
            
            # Band statistics
            band_power = np.sum(band_psd)
            band_energy = np.sum(band_magnitude**2)
            peak_in_band = np.max(band_magnitude)
            peak_freq_in_band = band_freqs[np.argmax(band_magnitude)]
            
            # Noise floor estimate (10th percentile)
            noise_floor = np.percentile(band_magnitude, 10)
            snr_band = 20 * np.log10(peak_in_band / noise_floor) if noise_floor > 0 else 0
            
            return {
                'frequency_range': (freq_low, freq_high),
                'num_samples': len(band_magnitude),
                'total_power': float(band_power),
                'total_energy': float(band_energy),
                'peak_magnitude': float(peak_in_band),
                'peak_frequency': float(peak_freq_in_band),
                'snr': float(snr_band),
                'noise_floor': float(noise_floor),
                'bandwidth': freq_high - freq_low,
                'info': f"✅ Band Analysis: {freq_low}-{freq_high} Hz, Power: {band_power:.2e}, SNR: {snr_band:.1f} dB"
            }
        
        except Exception as e:
            print(f"❌ Band Analysis Error: {str(e)}")
            return None
    
    @staticmethod
    def get_predefined_bands(spectrum_data):
        """
        Analyze common frequency bands (audio bands)
        
        Returns:
            dict with analysis of standard bands
        """
        bands = {
            'Sub-Bass': (20, 60),
            'Bass': (60, 250),
            'Low-Mid': (250, 500),
            'Mid': (500, 2000),
            'High-Mid': (2000, 4000),
            'Presence': (4000, 6000),
            'Brilliance': (6000, 20000),
        }
        
        results = {}
        for band_name, (low, high) in bands.items():
            analysis = FrequencyBandAnalyzer.extract_frequency_band(spectrum_data, low, high)
            if analysis:
                results[band_name] = analysis
        
        return results


class SignalComparator:
    """Compare two signals side-by-side"""
    
    @staticmethod
    def compare_signals(signal1, spectrum1, signal2, spectrum2):
        """
        Compare two signals
        
        Args:
            signal1, signal2: SignalData objects
            spectrum1, spectrum2: SpectrumData objects
        
        Returns:
            dict with comparison metrics
        """
        try:
            # Power comparison
            power1 = np.mean(np.abs(signal1.amplitude)**2)
            power2 = np.mean(np.abs(signal2.amplitude)**2)
            
            # RMS comparison
            rms1 = np.sqrt(np.mean(signal1.amplitude**2))
            rms2 = np.sqrt(np.mean(signal2.amplitude**2))
            
            # Peak comparison
            peak1 = np.max(np.abs(signal1.amplitude))
            peak2 = np.max(np.abs(signal2.amplitude))
            
            # Cross-correlation
            min_len = min(len(signal1.amplitude), len(signal2.amplitude))
            correlation = np.corrcoef(
                signal1.amplitude[:min_len],
                signal2.amplitude[:min_len]
            )[0, 1]
            
            # Frequency comparison
            freq_power1 = np.sum(spectrum1.psd)
            freq_power2 = np.sum(spectrum2.psd)
            
            return {
                'signal1_name': signal1.label,
                'signal2_name': signal2.label,
                'time_domain': {
                    'power_ratio': float(power1 / power2) if power2 > 0 else 0,
                    'rms_ratio': float(rms1 / rms2) if rms2 > 0 else 0,
                    'peak_ratio': float(peak1 / peak2) if peak2 > 0 else 0,
                    'correlation': float(correlation),
                },
                'frequency_domain': {
                    'freq_power_ratio': float(freq_power1 / freq_power2) if freq_power2 > 0 else 0,
                },
                'info': f"✅ Comparison Complete: Correlation: {correlation:.3f}"
            }
        
        except Exception as e:
            print(f"❌ Comparison Error: {str(e)}")
            return None
