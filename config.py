"""
Configuration file for PC Cleaner & Security Tool
"""
import os
from pathlib import Path

# Application Information
APP_NAME = "PC Cleaner & Security Tool"
APP_VERSION = "1.0.0"
APP_AUTHOR = "Your Name"

# Paths
BASE_DIR = Path(__file__).parent
RESOURCES_DIR = BASE_DIR / "resources"
LOGS_DIR = BASE_DIR / "logs"
QUARANTINE_DIR = BASE_DIR / "quarantine"

# Create directories if they don't exist
LOGS_DIR.mkdir(exist_ok=True)
QUARANTINE_DIR.mkdir(exist_ok=True)
RESOURCES_DIR.mkdir(exist_ok=True)

# Temp directories to scan
TEMP_DIRECTORIES = [
    os.environ.get('TEMP', ''),
    os.environ.get('TMP', ''),
    r'C:\Windows\Temp',
    os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Temp'),
]

# Browser cache paths
BROWSER_CACHE_PATHS = {
    'Chrome': os.path.join(os.environ.get('LOCALAPPDATA', ''), r'Google\Chrome\User Data\Default\Cache'),
    'Edge': os.path.join(os.environ.get('LOCALAPPDATA', ''), r'Microsoft\Edge\User Data\Default\Cache'),
    'Firefox': os.path.join(os.environ.get('LOCALAPPDATA', ''), r'Mozilla\Firefox\Profiles'),
}

# Protected system paths (never delete)
PROTECTED_PATHS = [
    r'C:\Windows\System32',
    r'C:\Windows\SysWOW64',
    r'C:\Program Files',
    r'C:\Program Files (x86)',
    r'C:\Windows\WinSxS',
]

# File extensions to consider as temporary
TEMP_FILE_EXTENSIONS = [
    '.tmp', '.temp', '.bak', '.old', '.cache', 
    '.log', '.dmp', '.chk', '~'
]

# Suspicious file patterns for malware detection
SUSPICIOUS_PATTERNS = [
    r'.*\.exe\.exe$',  # Double extension
    r'.*\.scr$',       # Screensaver files
    r'.*\.pif$',       # Program Information File
    r'.*\.bat\.exe$',  # Disguised batch files
]

# UI Theme
THEME_MODE = "dark"  # "dark" or "light"
COLOR_THEME = "blue"  # "blue", "green", "dark-blue"

# Logging
LOG_LEVEL = "INFO"
LOG_FILE = LOGS_DIR / "app.log"

# VirusTotal API (optional)
VIRUSTOTAL_API_KEY = ""  # Add your API key here if you have one
VIRUSTOTAL_ENABLED = False

# Scan settings
MAX_FILE_SIZE_MB = 100  # Maximum file size to scan (in MB)
SCAN_TIMEOUT_SECONDS = 300  # 5 minutes timeout for scans

# UI Settings
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700
