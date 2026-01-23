"""
File operation utilities for PC Cleaner & Security Tool
"""
import os
import shutil
import hashlib
from pathlib import Path
from typing import List, Dict, Tuple
import config


def calculate_directory_size(directory: str) -> int:
    """Calculate total size of a directory in bytes"""
    total_size = 0
    try:
        for dirpath, dirnames, filenames in os.walk(directory):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                try:
                    if os.path.exists(filepath):
                        total_size += os.path.getsize(filepath)
                except (OSError, PermissionError):
                    pass
    except (OSError, PermissionError):
        pass
    
    return total_size


def is_path_protected(path: str) -> bool:
    """Check if a path is in the protected paths list"""
    path = os.path.abspath(path)
    for protected in config.PROTECTED_PATHS:
        if path.startswith(protected):
            return True
    return False


def safe_delete_file(filepath: str) -> Tuple[bool, str]:
    """
    Safely delete a file with error handling
    Returns: (success: bool, message: str)
    """
    try:
        # Check if path is protected
        if is_path_protected(filepath):
            return False, "Protected system path - cannot delete"
        
        # Check if file exists
        if not os.path.exists(filepath):
            return False, "File does not exist"
        
        # Check permissions
        if not os.access(filepath, os.W_OK):
            return False, "Permission denied"
        
        # Delete the file
        os.remove(filepath)
        return True, "File deleted successfully"
    
    except PermissionError:
        return False, "Permission denied"
    except Exception as e:
        return False, f"Error: {str(e)}"


def safe_delete_directory(directory: str) -> Tuple[bool, str]:
    """
    Safely delete a directory with error handling
    Returns: (success: bool, message: str)
    """
    try:
        # Check if path is protected
        if is_path_protected(directory):
            return False, "Protected system path - cannot delete"
        
        # Check if directory exists
        if not os.path.exists(directory):
            return False, "Directory does not exist"
        
        # Delete the directory
        shutil.rmtree(directory)
        return True, "Directory deleted successfully"
    
    except PermissionError:
        return False, "Permission denied"
    except Exception as e:
        return False, f"Error: {str(e)}"


def get_file_hash(filepath: str, algorithm: str = 'md5') -> str:
    """Calculate hash of a file"""
    try:
        hash_obj = hashlib.new(algorithm)
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                hash_obj.update(chunk)
        return hash_obj.hexdigest()
    except Exception as e:
        return ""


def move_to_quarantine(filepath: str) -> Tuple[bool, str]:
    """
    Move a file to quarantine directory
    Returns: (success: bool, message: str)
    """
    try:
        filename = os.path.basename(filepath)
        quarantine_path = config.QUARANTINE_DIR / filename
        
        # If file with same name exists, add timestamp
        if quarantine_path.exists():
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            name, ext = os.path.splitext(filename)
            quarantine_path = config.QUARANTINE_DIR / f"{name}_{timestamp}{ext}"
        
        shutil.move(filepath, quarantine_path)
        return True, f"Moved to quarantine: {quarantine_path}"
    
    except Exception as e:
        return False, f"Error moving to quarantine: {str(e)}"


def get_file_info(filepath: str) -> Dict[str, any]:
    """Get detailed information about a file"""
    try:
        stat = os.stat(filepath)
        return {
            'path': filepath,
            'name': os.path.basename(filepath),
            'size': stat.st_size,
            'created': stat.st_ctime,
            'modified': stat.st_mtime,
            'accessed': stat.st_atime,
            'is_hidden': bool(os.stat(filepath).st_file_attributes & 2) if os.name == 'nt' else False,
        }
    except Exception as e:
        return {'error': str(e)}


def scan_directory_for_files(directory: str, extensions: List[str] = None, 
                             max_depth: int = None) -> List[str]:
    """
    Scan directory for files with specific extensions
    Args:
        directory: Directory to scan
        extensions: List of file extensions to include (e.g., ['.tmp', '.log'])
        max_depth: Maximum depth to scan (None for unlimited)
    Returns:
        List of file paths
    """
    found_files = []
    
    try:
        for root, dirs, files in os.walk(directory):
            # Calculate current depth
            if max_depth is not None:
                depth = root[len(directory):].count(os.sep)
                if depth >= max_depth:
                    dirs.clear()  # Don't recurse deeper
            
            for file in files:
                filepath = os.path.join(root, file)
                
                # If extensions specified, filter by extension
                if extensions:
                    if any(file.lower().endswith(ext.lower()) for ext in extensions):
                        found_files.append(filepath)
                else:
                    found_files.append(filepath)
    
    except (PermissionError, OSError):
        pass
    
    return found_files
