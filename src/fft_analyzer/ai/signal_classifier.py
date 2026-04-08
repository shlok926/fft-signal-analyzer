"""
Signal Classification using Neural Networks
Classifies signals into categories: Normal, Transient, Periodic, Chaotic, Noisy
"""

import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from typing import Dict, Any, Tuple
import streamlit as st

from ..utils import logger


class SignalClassifier:
    """AI-powered signal classification using Neural Networks"""
    
    # Signal categories
    CATEGORIES = ['Normal', 'Transient', 'Periodic', 'Chaotic', 'Noisy']
    
    @staticmethod
    def extract_features(signal_data: Any, spectrum_data: Any) -> np.ndarray:
        """
        Extract comprehensive features from signal and spectrum
        
        Args:
            signal_data: SignalData object
            spectrum_data: SpectrumData object
            
        Returns:
            Feature vector (1D numpy array)
        """
        try:
            amplitude = signal_data.amplitude
            magnitude = spectrum_data.magnitude
            
            # Time-domain features
            time_features = [
                np.mean(amplitude),                    # Mean
                np.std(amplitude),                     # Std Dev
                np.max(amplitude),                     # Peak
                np.min(amplitude),                     # Trough
                np.sqrt(np.mean(amplitude ** 2)),      # RMS
            ]
            
            # Statistical features
            from scipy import stats
            statistical_features = [
                float(stats.skew(amplitude)),          # Skewness
                float(stats.kurtosis(amplitude)),      # Kurtosis
                np.percentile(amplitude, 25),          # Q1
                np.percentile(amplitude, 75),          # Q3
            ]
            
            # Frequency-domain features
            frequency_features = [
                np.max(magnitude),                     # Peak magnitude
                np.argmax(magnitude),                  # Dominant frequency index
                np.sum(magnitude),                     # Total energy
                np.std(magnitude),                     # Spectral std
            ]
            
            # Spectral centroid
            frequencies = spectrum_data.freqs
            spectral_centroid = np.sum(frequencies * magnitude) / np.sum(magnitude) if np.sum(magnitude) > 0 else 0
            
            # Spectral bandwidth
            spectral_bandwidth = np.sqrt(
                np.sum(((frequencies - spectral_centroid) ** 2) * magnitude) / np.sum(magnitude)
            ) if np.sum(magnitude) > 0 else 0
            
            spectral_features = [
                float(spectral_centroid),
                float(spectral_bandwidth),
                np.ptp(magnitude),                     # Peak-to-peak
                np.median(magnitude),                  # Median magnitude
            ]
            
            # Combine all features
            features = np.array(time_features + statistical_features + 
                              frequency_features + spectral_features)
            
            print(f"🔍 Extracted {len(features)} features from signal")
            
            return features
            
        except Exception as e:
            logger.error(f"Feature extraction error: {str(e)}")
            return None
    
    @staticmethod
    def classify_signal(signal_data: Any, spectrum_data: Any) -> Dict[str, Any]:
        """
        Classify signal using heuristic rules (rule-based classifier)
        
        Note: For production, train an actual MLPClassifier on labeled data
        
        Args:
            signal_data: SignalData object
            spectrum_data: SpectrumData object
            
        Returns:
            Dictionary with classification results
        """
        try:
            print("\n" + "="*60)
            print("🧠 SIGNAL CLASSIFICATION STARTED")
            print("="*60)
            
            # Extract features
            features = SignalClassifier.extract_features(signal_data, spectrum_data)
            
            if features is None:
                return None
            
            amplitude = signal_data.amplitude
            magnitude = spectrum_data.magnitude
            
            # Rule-based classification (until proper model is trained)
            # These are heuristics based on signal characteristics
            
            scores = {
                'Normal': 0.0,
                'Transient': 0.0,
                'Periodic': 0.0,
                'Chaotic': 0.0,
                'Noisy': 0.0
            }
            
            # Feature 1: Periodicity (check for repeated patterns)
            autocorr = np.correlate(amplitude, amplitude, mode='full')
            autocorr = autocorr / np.max(autocorr)
            periodicity_score = np.max(autocorr[len(autocorr)//2+1:len(autocorr)//2+100])
            
            # Feature 2: Transient detection (sudden changes)
            diff = np.diff(amplitude)
            transient_score = len(np.where(np.abs(diff) > 3*np.std(diff))[0]) / len(amplitude)
            
            # Feature 3: Noise level (high frequency content)
            high_freq_energy = np.sum(magnitude[-len(magnitude)//4:]) / np.sum(magnitude)
            noise_score = high_freq_energy
            
            # Feature 4: Chaos (Lyapunov-like metric)
            entropy = -np.sum(magnitude * np.log(magnitude + 1e-10)) / len(magnitude)
            chaos_score = entropy / 10  # Normalize
            
            # Feature 5: Normality (low entropy, regular behavior)
            normality_score = 1 - (transient_score + noise_score + chaos_score) / 3
            
            # Assign scores based on combinations
            if periodicity_score > 0.6:
                scores['Periodic'] += 0.8
            
            if transient_score > 0.15:
                scores['Transient'] += 0.7
            
            if noise_score > 0.5:
                scores['Noisy'] += 0.8
            
            if chaos_score > 0.5:
                scores['Chaotic'] += 0.7
            
            if normality_score > 0.5:
                scores['Normal'] += 0.8
            
            # Normalize scores
            total_score = sum(scores.values())
            if total_score > 0:
                scores = {k: v/total_score for k, v in scores.items()}
            else:
                scores = {k: 1/len(scores) for k in scores}
            
            # Get primary and secondary classifications
            sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
            primary_class = sorted_scores[0][0]
            primary_confidence = sorted_scores[0][1]
            secondary_class = sorted_scores[1][0]
            secondary_confidence = sorted_scores[1][1]
            
            info = f"""
            ✅ Classification Complete:
            • Primary Class: {primary_class} ({primary_confidence*100:.1f}%)
            • Secondary Class: {secondary_class} ({secondary_confidence*100:.1f}%)
            • Periodicity: {periodicity_score*100:.1f}%
            • Transient Activity: {transient_score*100:.1f}%
            • Noise Level: {noise_score*100:.1f}%
            • Chaos Index: {chaos_score*100:.1f}%
            • Method: Heuristic Rule-Based Classifier
            """
            
            print(info)
            print("="*60)
            
            return {
                'primary_class': primary_class,
                'primary_confidence': primary_confidence,
                'secondary_class': secondary_class,
                'secondary_confidence': secondary_confidence,
                'all_scores': scores,
                'features': features,
                'periodicity': periodicity_score,
                'transient': transient_score,
                'noise_level': noise_score,
                'chaos': chaos_score,
                'info': info
            }
            
        except Exception as e:
            print(f"❌ Classification Error: {str(e)}")
            import traceback
            traceback.print_exc()
            st.error(f"Classification Error: {str(e)}")
            return None
