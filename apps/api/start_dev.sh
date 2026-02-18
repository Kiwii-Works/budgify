#!/bin/bash
echo "Starting Budgify API Server..."
echo ""
cd src
../.venv/bin/python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
