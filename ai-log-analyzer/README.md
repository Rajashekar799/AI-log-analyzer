# AI Log Analyzer

An AI-powered log analysis tool that uses machine learning to detect patterns, anomalies, and suggest root causes from multi-source logs. Built with FastAPI, scikit-learn, and pandas.

## Features

- **Log Collection**: Aggregate logs from files or text input with automatic parsing
- **ML-Powered Analysis**: Uses TF-IDF vectorization, Isolation Forest for anomaly detection, and KMeans clustering for pattern recognition
- **Root Cause Suggestions**: Provides actionable insights based on detected issues
- **Web Dashboard**: Simple HTML interface for uploading logs and viewing analysis results
- **REST API**: Programmatic access via FastAPI endpoints

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Installation

1. **Clone or navigate to the project directory**:
   ```bash
   cd ai-log-analyzer
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

   This will install:
   - fastapi
   - uvicorn
   - scikit-learn
   - pandas
   - numpy
   - python-multipart

## Running the Application

1. **Start the FastAPI server**:
   ```bash
   python app.py
   ```

   The server will start on `http://127.0.0.1:8000`

2. **Access the web dashboard**:
   Open your browser and go to `http://127.0.0.1:8000`

## Usage

### Web Dashboard
- Upload log files (.log or .txt) using the file input
- Or paste log text directly in the textarea
- Click "Analyze Logs" to process and view results
- Results include detected patterns, anomalies, and root cause suggestions

### API Endpoints

#### Analyze Text Logs
```bash
POST /analyze-text-logs
Content-Type: application/json

{
  "logs": [
    "2023-10-01 10:00:00 INFO Application started",
    "2023-10-01 10:05:00 ERROR Database connection failed"
  ]
}
```

#### Upload Log Files
```bash
POST /upload-logs
Content-Type: multipart/form-data

file: [log file]
```

### Sample Logs
Use the provided `sample_logs.txt` file to test the system with example log entries.

## Project Structure

```
ai-log-analyzer/
├── app.py                 # Main FastAPI application
├── log_collector.py       # Log parsing and preprocessing
├── ml_engine.py          # Machine learning models
├── root_cause_suggester.py # Root cause analysis
├── requirements.txt      # Python dependencies
├── sample_logs.txt       # Example log data
├── static/
│   └── index.html        # Web dashboard
└── README.md            # This file
```

## API Response Format

```json
{
  "message": "Logs analyzed successfully",
  "analysis": {
    "patterns": {"0": 5, "1": 3, "2": 2},
    "anomalies": [
      {
        "timestamp": "2023-10-01T10:05:00",
        "level": "ERROR",
        "message": "Database connection failed",
        "source": "unknown"
      }
    ],
    "anomaly_scores": [0.1, -0.2, 0.0]
  },
  "root_cause_suggestions": [
    "Check database connectivity",
    "Review network configuration"
  ]
}
```

## Troubleshooting

- **Port already in use**: Kill existing processes on port 8000 or change the port in `app.py`
- **Import errors**: Ensure all dependencies are installed with `pip install -r requirements.txt`
- **ML errors with small datasets**: The system automatically adjusts clustering for small log sets

## Future Enhancements

- Integration with ELK stack for real-time log streaming
- Pre-trained models for faster analysis
- Advanced visualization dashboards
- Alert system for critical anomalies

## License

This project is open-source. Feel free to modify and distribute.
