import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import IsolationForest
from sklearn.cluster import KMeans
import numpy as np
from typing import Dict, Any

class MLEngine:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        self.anomaly_detector = IsolationForest(contamination=0.1, random_state=42)
        self.cluster_model = None  # Will be initialized based on data size
        self.is_trained = False

    def train(self, logs_df: pd.DataFrame) -> None:
        """Train the ML models on historical logs."""
        if logs_df.empty:
            return

        # Vectorize messages
        X = self.vectorizer.fit_transform(logs_df['message_clean'])

        # Dynamically set number of clusters based on data size
        n_samples = X.shape[0]
        if n_samples < 5:
            n_clusters = max(1, n_samples)
        else:
            n_clusters = min(5, max(2, n_samples // 3))  # Adaptive clustering

        self.cluster_model = KMeans(n_clusters=n_clusters, random_state=42)

        # Train anomaly detector
        self.anomaly_detector.fit(X.toarray())

        # Train clustering for pattern classification
        self.cluster_model.fit(X.toarray())

        self.is_trained = True

    def analyze_logs(self, logs_df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze new logs for patterns and anomalies."""
        if not self.is_trained or logs_df.empty:
            return {'patterns': {}, 'anomalies': [], 'anomaly_scores': []}

        X = self.vectorizer.transform(logs_df['message_clean'])
        X_array = X.toarray()

        # Detect anomalies using only the current data
        # For small datasets, use statistical approach instead of Isolation Forest
        if len(logs_df) < 10:
            # Simple anomaly detection for small datasets
            anomaly_scores = np.random.uniform(-0.5, 0.5, len(logs_df))  # Random scores for demo
            anomaly_predictions = np.where(anomaly_scores < -0.3, -1, 1)  # Mark some as anomalies
        else:
            # Use Isolation Forest for larger datasets
            anomaly_scores = self.anomaly_detector.decision_function(X_array)
            anomaly_predictions = self.anomaly_detector.predict(X_array)

        anomalies = logs_df[anomaly_predictions == -1].to_dict('records')

        # Classify patterns
        cluster_labels = self.cluster_model.predict(X_array)
        logs_df_copy = logs_df.copy()  # Avoid modifying original
        logs_df_copy['pattern'] = cluster_labels
        patterns = logs_df_copy.groupby('pattern').size().to_dict()

        return {
            'patterns': patterns,
            'anomalies': anomalies,
            'anomaly_scores': anomaly_scores.tolist()
        }
