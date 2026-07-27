#!/bin/bash
# Social Media Engine - Dashboard Launcher

echo "🚀 Social Media Engine - Dashboard"
echo "=================================="
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

# Check if pip is available
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is required but not installed."
    exit 1
fi

# Install Flask if not already installed
echo "📦 Checking dependencies..."
pip3 install flask flask-cors -q

# Start the dashboard
echo "✅ Dependencies ready"
echo ""
echo "🌐 Starting dashboard..."
echo "📊 Open browser: http://localhost:5000"
echo "🛑 Press Ctrl+C to stop"
echo ""

cd "$(dirname "$0")"
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
python3 src/dashboard/app.py
