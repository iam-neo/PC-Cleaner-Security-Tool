"""
Build script for creating standalone executable
"""
import PyInstaller.__main__
import os
import shutil

# Clean previous builds
if os.path.exists('build'):
    shutil.rmtree('build')
if os.path.exists('dist'):
    shutil.rmtree('dist')

# PyInstaller arguments
PyInstaller.__main__.run([
    'pc_cleaner_app.py',
    '--name=PCCleanerTool',
    '--onefile',
    '--windowed',
    '--icon=resources/icon.png',
    '--add-data=resources;resources',
    '--hidden-import=customtkinter',
    '--hidden-import=PIL',
    '--hidden-import=psutil',
    '--hidden-import=requests',
    '--clean',
])

print("\n" + "="*50)
print("Build complete!")
print("Executable location: dist/PCCleanerTool.exe")
print("="*50)
