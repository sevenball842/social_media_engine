"""
Build standalone Windows executable using PyInstaller
Run: python build_exe.py
"""

import PyInstaller.__main__
import os
import shutil
from pathlib import Path

# Clean old builds
if os.path.exists('build'):
    shutil.rmtree('build')
if os.path.exists('dist'):
    shutil.rmtree('dist')

# Get paths
src_dir = os.path.dirname(os.path.abspath(__file__))
dashboard_dir = os.path.join(src_dir, 'src', 'dashboard')
launcher_file = os.path.join(src_dir, 'launcher.py')

print("🔨 Building Social Media Engine executable...")
print(f"Source: {src_dir}")

# Build with PyInstaller
PyInstaller.__main__.run([
    launcher_file,
    '--name=SocialMediaEngine',
    '--onefile',
    '--console',
    '--add-data', f'{dashboard_dir}/templates:templates',
    '--add-data', f'{dashboard_dir}/static:static',
    '--hidden-import=flask',
    '--hidden-import=flask_cors',
    '--hidden-import=werkzeug',
    '--hidden-import=jinja2',
    '--hidden-import=click',
    '--hidden-import=src.dashboard',
    '--hidden-import=src.content_manager',
    '--hidden-import=src.status_calculator',
    '--hidden-import=src.approval_workflow',
    '--hidden-import=src.scheduler',
    '--hidden-import=src.performance_tracker',
    '--clean',
    '--noconfirm',
])

exe_path = os.path.join('dist', 'SocialMediaEngine.exe')
print("\n✅ Build complete!")
print(f"📦 Executable: {exe_path}")
print(f"\n📋 Next steps:")
print(f"1. Copy '{exe_path}' to your preferred location")
print(f"2. Double-click to launch the dashboard")
print(f"3. Browser will open automatically at http://localhost:5000")
