#!/bin/bash

echo "========================================"
echo " Smart Student Performance Predictor"
echo "========================================"
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt
echo ""
echo "Starting application..."
echo ""
echo "Open your browser and go to:"
echo "http://localhost:5000"
echo ""
echo "Login credentials:"
echo "Username: admin"
echo "Password: admin123"
echo ""
python app.py
