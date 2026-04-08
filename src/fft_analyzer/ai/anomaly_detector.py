"""
Anomaly Detection using Isolation Forest
Detects unusual patterns in signal and spectrum
"""

import numpy as np
from sklearn.ensemble import IsolationForest
from typing import Dict, Any, Tuple
import streamlit as st

from ..utils import logger


class AnomalyDetector:
    """AI-powered anomaly detection using Isolation Forest"""
    
    @staticmethod
    def detect_spectrum_anomalies(spectrum_data: Any, contamination: float = 0.1) -> Dict[str, Any]:
        """
        Detect anomalies in frequency spectrum
        
        Args:
            spectrum_data: SpectrumData object
            contamination: Expected proportion of anomalies (0.0-1.0)
        
        Returns:
            Dictionary with:
            - anomaly_scores: Anomaly score for each frequency (-1 to 1)
            - is_anomaly: Boolean array (True = anomaly)
            - anomaly_indices: Indices of anomalous frequencies
            - anomaly_count: Number of anomalies detected
            - severity: Average anomaly severity (0-1)
            - info: String with metrics
        """
        try:
            print("\n" + "="*60)
            print("🔴 ANOMALY DETECTION STARTED")
            print("="*60)
            
            # Prepare feature matrix
            # Use magnitude and PSD for anomaly detection
            features = np.vstack([
                spectrum_data.magnitude,
                spectrum_data.psd,
                # Add derivative (rate of change)
                np.gradient(spectrum_data.magnitude),
                np.gradient(spectrum_data.psd)
            ]).T
            
            print(f"Features shape: {features.shape}")
            print(f"Contamination: {contamination*100:.1f}%")
            
            # Apply Isolation Forest
            iso_forest = IsolationForest(
                contamination=contamination,
                random_state=42,
                n_estimators=100
            )
            
            # Get predictions (-1 = anomaly, 1 = normal)
            predictions = iso_forest.fit_predict(features)
            
            # Get anomaly scores (-1.0 to 1.0, where more negative = more anomalous)
            anomaly_scores = iso_forest.score_samples(features)
            
            # Normalize scores to 0-1 (0 = normal, 1 = anomaly)
            anomaly_scores_normalized = -((anomaly_scores - anomaly_scores.min()) / 
                                         (anomaly_scores.max() - anomaly_scores.min()))
            
            is_anomaly = predictions == -1
            anomaly_indices = np.where(is_anomaly)[0]
            anomaly_count = is_anomaly.sum()
            
            # Severity metrics
            severity = anomaly_scores_normalized[is_anomaly].mean() if anomaly_count > 0 else 0
            
            # Get top anomalies
            top_indices = np.argsort(anomaly_scores_normalized)[-5:][::-1]
            top_anomalies = [
                {
                    'freq': spectrum_data.freqs[i],
                    'magnitude': spectrum_data.magnitude[i],
                    'score': anomaly_scores_normalized[i]
                }
                for i in top_indices if is_anomaly[i]
            ]
            
            info = f"""
            ✅ Anomaly Detection Complete:
            • Anomalies Found: {anomaly_count} ({anomaly_count/len(predictions)*100:.1f}%)
            • Severity: {severity*100:.1f}%
            • High-risk frequencies: {len(top_anomalies)}
            • Detection Method: Isolation Forest (100 estimators)
            • Features: Magnitude, PSD, Gradients
            """
            
            print(info)
            print("="*60)
            
            return {
                'anomaly_scores': anomaly_scores_normalized,
                'is_anomaly': is_anomaly,
                'anomaly_indices': anomaly_indices,
                'anomaly_count': anomaly_count,
                'severity': severity,
                'top_anomalies': top_anomalies,
                'model': iso_forest,
                'info': info
            }
            
        except Exception as e:
            print(f"❌ Anomaly Detection Error: {str(e)}")
            import traceback
            traceback.print_exc()
            st.error(f"Anomaly Detection Error: {str(e)}")
            return None
    
    @staticmethod
    def detect_signal_anomalies(signal_data: Any, contamination: float = 0.05) -> Dict[str, Any]:
        """
        Detect anomalies in time-domain signal
        
        Args:
            signal_data: SignalData object
            contamination: Expected anomaly ratio
        
        Returns:
            Dictionary with anomaly detection results
        """
        try:
            # Create features from signal
            amplitude = signal_data.amplitude
            
            # Calculate local statistics in windows
            window_size = min(64, len(amplitude) // 4)
            features_list = []
            
            for i in range(0, len(amplitude), window_size):
                window = amplitude[i:i+window_size]
                if len(window) > 0:
                    features_list.append([
                        np.mean(window),
                        np.std(window),
                        np.max(window),
                        np.min(window),
                    ])
            
            features = np.array(features_list)
            
            iso_forest = IsolationForest(
                contamination=contamination,
                random_state=42
            )
            
            predictions = iso_forest.fit_predict(features)
            anomaly_scores = -iso_forest.score_samples(features)
            
            # Normalize
            anomaly_scores_norm = (anomaly_scores - anomaly_scores.min()) / (anomaly_scores.max() - anomaly_scores.min() + 1e-10)
            
            is_anomaly = predictions == -1
            
            return {
                'anomaly_scores': anomaly_scores_norm,
                'is_anomaly': is_anomaly,
                'window_size': window_size,
                'anomaly_count': is_anomaly.sum(),
                'severity': anomaly_scores_norm[is_anomaly].mean() if is_anomaly.sum() > 0 else 0,
                'model': iso_forest
            }
            
        except Exception as e:
            logger.error(f"Signal anomaly detection error: {str(e)}")
            return None
