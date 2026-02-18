@echo off
echo Starting Budgify API Server...
echo.
cd src
..\.venv\Scripts\python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
