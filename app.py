from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import os
from log_collector import LogCollector
from ml_engine import MLEngine
from root_cause_suggester import RootCauseSuggester
import json



app = FastAPI(title="AI Assisted Root Cause Suggestion from Multi-Source Logs", description="AI-assisted root cause suggestion from multi-source logs")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")



@app.get("/", response_class=HTMLResponse)
async def get_dashboard():
    """Serve the web dashboard."""
    try:
        static_dir = os.path.join(os.path.dirname(__file__), "static")
        html_path = os.path.join(static_dir, "index.html")
        with open(html_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "<h1>Dashboard not found. Please ensure static/index.html exists.</h1>"
    except UnicodeDecodeError:
        # Fallback for encoding issues
        with open(html_path, "rb") as f:
            content = f.read().decode("utf-8", errors="replace")
            return content

@app.post("/upload-logs")
async def upload_logs(file: UploadFile = File(...)):
    """Upload and analyze log files."""
    if not file.filename.endswith(('.log', '.txt')):
        raise HTTPException(status_code=400, detail="Only .log or .txt files are supported.")

    # Save uploaded file temporarily
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as f:
        content = await file.read()
        f.write(content)

    try:
        # Initialize fresh components for each request
        log_collector = LogCollector()
        ml_engine = MLEngine()
        root_cause_suggester = RootCauseSuggester()

        # Collect logs
        log_collector.collect_from_file(temp_path)
        logs_df = log_collector.get_logs_df()

        if logs_df.empty:
            raise HTTPException(status_code=400, detail="No valid logs found in the file.")

        # Train ML model (in production, use pre-trained model)
        ml_engine.train(logs_df)

        # Analyze logs
        analysis_results = ml_engine.analyze_logs(logs_df)

        # Suggest root causes
        suggestions = root_cause_suggester.suggest_root_causes(analysis_results)

        # Clean up
        os.remove(temp_path)

        return {
            "message": "Logs analyzed successfully",
            "analysis": analysis_results,
            "root_cause_suggestions": suggestions
        }

    except Exception as e:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        raise HTTPException(status_code=500, detail=f"Error processing logs: {str(e)}")

@app.post("/analyze-text-logs")
async def analyze_text_logs(logs: dict):
    """Analyze logs provided as text."""
    log_lines = logs.get("logs", [])
    if not log_lines:
        raise HTTPException(status_code=400, detail="No logs provided.")

    try:
        # Initialize fresh components for each request
        log_collector = LogCollector()
        ml_engine = MLEngine()
        root_cause_suggester = RootCauseSuggester()

        # Collect logs
        log_collector.collect_from_list(log_lines)
        logs_df = log_collector.get_logs_df()

        if logs_df.empty:
            raise HTTPException(status_code=400, detail="No valid log entries found. Please ensure logs follow the expected format (e.g., '2023-10-01 10:00:00 INFO message' or '2025-10-26T10:15:42 - INFO: [Service] - message').")

        # Train and analyze
        ml_engine.train(logs_df)
        analysis_results = ml_engine.analyze_logs(logs_df)
        suggestions = root_cause_suggester.suggest_root_causes(analysis_results)

        return {
            "message": "Logs analyzed successfully",
            "analysis": analysis_results,
            "root_cause_suggestions": suggestions
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing logs: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
