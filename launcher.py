"""
Social Media Engine Launcher
Opens Flask dashboard in browser automatically
"""

import os
import sys
import webbrowser
from threading import Timer
from pathlib import Path

# Ensure we're in the right directory
if getattr(sys, 'frozen', False):
    os.chdir(os.path.dirname(sys.executable))

# Import after directory setup
from src.dashboard.app import app

def open_browser():
    """Open browser to dashboard after Flask starts"""
    webbrowser.open('http://127.0.0.1:5000')

if __name__ == '__main__':
    print("\n" + "="*50)
    print("  🚀 Social Media Engine Dashboard")
    print("="*50)
    print("\n📊 Opening dashboard in your browser...")
    print("📍 http://localhost:5000\n")

    # Open browser after short delay to let Flask start
    timer = Timer(2.0, open_browser)
    timer.daemon = True
    timer.start()

    try:
        app.run(debug=False, host='127.0.0.1', port=5000, use_reloader=False)
    except KeyboardInterrupt:
        print("\n\n✅ Dashboard stopped")
        sys.exit(0)
