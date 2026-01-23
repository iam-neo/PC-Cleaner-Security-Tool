"""
System information utilities for PC Cleaner & Security Tool
"""
import os
import psutil
import platform
from pathlib import Path
from typing import Dict, List


def get_disk_usage() -> Dict[str, any]:
    """Get disk usage statistics for the system drive"""
    try:
        disk = psutil.disk_usage('C:\\')
        return {
            'total': disk.total,
            'used': disk.used,
            'free': disk.free,
            'percent': disk.percent,
            'total_gb': round(disk.total / (1024**3), 2),
            'used_gb': round(disk.used / (1024**3), 2),
            'free_gb': round(disk.free / (1024**3), 2),
        }
    except Exception as e:
        return {'error': str(e)}


def get_system_info() -> Dict[str, str]:
    """Get basic system information"""
    return {
        'os': platform.system(),
        'os_version': platform.version(),
        'os_release': platform.release(),
        'machine': platform.machine(),
        'processor': platform.processor(),
        'python_version': platform.python_version(),
    }


def get_running_processes() -> List[Dict[str, any]]:
    """Get list of running processes"""
    processes = []
    try:
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                processes.append({
                    'pid': proc.info['pid'],
                    'name': proc.info['name'],
                    'cpu_percent': proc.info['cpu_percent'],
                    'memory_percent': proc.info['memory_percent'],
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
    except Exception as e:
        print(f"Error getting processes: {e}")
    
    return processes


def get_temp_directories() -> List[str]:
    """Get list of temporary directories on the system"""
    temp_dirs = []
    
    # Standard Windows temp directories
    temp_locations = [
        os.environ.get('TEMP'),
        os.environ.get('TMP'),
        r'C:\Windows\Temp',
        os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Temp'),
    ]
    
    for temp_dir in temp_locations:
        if temp_dir and os.path.exists(temp_dir):
            temp_dirs.append(temp_dir)
    
    return list(set(temp_dirs))  # Remove duplicates


def get_browser_cache_paths() -> Dict[str, str]:
    """Get browser cache directory paths"""
    cache_paths = {}
    
    localappdata = os.environ.get('LOCALAPPDATA', '')
    appdata = os.environ.get('APPDATA', '')
    
    browsers = {
        'Chrome': os.path.join(localappdata, r'Google\Chrome\User Data\Default\Cache'),
        'Edge': os.path.join(localappdata, r'Microsoft\Edge\User Data\Default\Cache'),
        'Firefox': os.path.join(appdata, r'Mozilla\Firefox\Profiles'),
        'Opera': os.path.join(appdata, r'Opera Software\Opera Stable\Cache'),
    }
    
    for browser, path in browsers.items():
        if os.path.exists(path):
            cache_paths[browser] = path
    
    return cache_paths


def format_bytes(bytes_size: int) -> str:
    """Format bytes to human-readable format"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.2f} PB"


def is_admin() -> bool:
    """Check if the application is running with administrator privileges"""
    try:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except:
        return False


def get_user_profile_path() -> str:
    """Get the current user's profile path"""
    return os.environ.get('USERPROFILE', '')
