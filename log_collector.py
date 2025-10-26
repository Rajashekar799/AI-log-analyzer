import pandas as pd
import re
from typing import List, Dict, Any
import pytz

class LogCollector:
    def __init__(self):
        self.logs = []

    def collect_from_file(self, file_path: str) -> None:
        """Collect logs from a file."""
        try:
            with open(file_path, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    parsed_log = self.parse_log_line(line.strip())
                    if parsed_log:
                        self.logs.append(parsed_log)
        except FileNotFoundError:
            print(f"File {file_path} not found.")

    def collect_from_list(self, log_lines: List[str]) -> None:
        """Collect logs from a list of strings."""
        for line in log_lines:
            parsed_log = self.parse_log_line(line)
            if parsed_log:
                self.logs.append(parsed_log)

    def parse_log_line(self, line: str) -> Dict[str, Any]:
        """Parse a single log line into structured format."""
        # Updated regex to match common log formats
        # Format 1: 2023-10-01 10:00:00 INFO message
        pattern1 = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) (\w+) (.+)'
        # Format 2: 2025-10-26T10:15:42 - INFO: [Service] - message
        pattern2 = r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}) - (\w+): \[([^\]]+)\] - (.+)'

        match = re.match(pattern1, line.strip())
        if match:
            timestamp, level, message = match.groups()
            return {
                'timestamp': timestamp,
                'level': level,
                'message': message,
                'source': 'unknown'
            }

        match = re.match(pattern2, line.strip())
        if match:
            timestamp, level, service, message = match.groups()
            return {
                'timestamp': timestamp,
                'level': level,
                'message': f"[{service}] - {message}",
                'source': service
            }

        return None

    def preprocess_logs(self) -> pd.DataFrame:
        """Preprocess and normalize logs into a DataFrame."""
        df = pd.DataFrame(self.logs)
        if not df.empty:
            df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
            # Convert to IST timezone
            ist = pytz.timezone('Asia/Kolkata')
            df['timestamp'] = df['timestamp'].dt.tz_localize('UTC').dt.tz_convert(ist)
            df['message_clean'] = df['message'].apply(self.clean_message)
        return df

    def clean_message(self, message: str) -> str:
        """Clean and normalize log messages."""
        # Remove special characters, lowercase, etc.
        message = re.sub(r'[^\w\s]', '', message)
        return message.lower()

    def get_logs_df(self) -> pd.DataFrame:
        """Return the collected logs as a DataFrame."""
        return self.preprocess_logs()
