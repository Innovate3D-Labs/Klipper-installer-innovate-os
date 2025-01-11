#!/bin/bash

# Start nginx
service nginx start

# Start the FastAPI application
cd /app
uvicorn backend.main:app --host 0.0.0.0 --port 8000
