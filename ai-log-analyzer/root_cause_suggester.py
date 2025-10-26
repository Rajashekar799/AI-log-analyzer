from typing import List, Dict, Any

class RootCauseSuggester:
    def __init__(self):
        # Simple rule-based mapping of patterns to root causes
        self.pattern_to_cause = {
            0: "Database connection timeout - Check DB server status",
            1: "Memory leak detected - Monitor application memory usage",
            2: "Network connectivity issue - Verify network configuration",
            3: "Authentication failure - Review user credentials",
            4: "High CPU usage - Optimize code or scale resources"
        }

    def suggest_root_causes(self, analysis_results: Dict[str, Any]) -> List[str]:
        """Suggest root causes based on analysis results."""
        suggestions = []

        # Based on anomalies
        if analysis_results['anomalies']:
            suggestions.append("Anomalies detected: Investigate unusual log patterns for potential issues.")

        # Based on patterns
        for pattern, count in analysis_results['patterns'].items():
            if count > 5:  # Threshold for frequent patterns
                cause = self.pattern_to_cause.get(pattern, f"Unknown pattern {pattern} - Manual investigation required")
                suggestions.append(f"Frequent pattern {pattern}: {cause}")

        # If no specific suggestions, provide general advice
        if not suggestions:
            suggestions.append("No significant patterns detected. System appears normal.")

        return suggestions

    def update_historical_data(self, logs_df, analysis_results):
        """Update historical data for better future suggestions (placeholder)."""
        # In a real system, this would store data in a database
        pass
