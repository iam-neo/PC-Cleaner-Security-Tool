"""
PC Cleaner Module - Scans and removes temporary files and cache
"""
import os
import threading
from typing import List, Dict, Callable, Tuple
from pathlib import Path
from utils.file_operations import (
    calculate_directory_size, 
    safe_delete_file, 
    scan_directory_for_files,
    is_path_protected
)
from utils.system_info import get_temp_directories, get_browser_cache_paths, format_bytes
import config


class PCCleaner:
    def __init__(self):
        self.scan_results = {
            'temp_files': [],
            'browser_cache': [],
            'system_cache': [],
        }
        self.total_size = 0
        self.is_scanning = False
        self.scan_progress = 0
        self.current_file = ""
        
    def scan_temp_files(self, progress_callback: Callable = None) -> Dict:
        """Scan for temporary files in system temp directories"""
        temp_files = []
        total_size = 0
        
        temp_dirs = get_temp_directories()
        
        for temp_dir in temp_dirs:
            if progress_callback:
                progress_callback(f"Scanning: {temp_dir}")
            
            try:
                # Scan for files with temp extensions
                files = scan_directory_for_files(temp_dir, config.TEMP_FILE_EXTENSIONS)
                
                for filepath in files:
                    try:
                        if not is_path_protected(filepath):
                            size = os.path.getsize(filepath)
                            temp_files.append({
                                'path': filepath,
                                'size': size,
                                'size_formatted': format_bytes(size),
                                'category': 'Temporary Files',
                                'location': temp_dir,
                            })
                            total_size += size
                    except (OSError, PermissionError):
                        pass
            
            except Exception as e:
                print(f"Error scanning {temp_dir}: {e}")
        
        return {
            'files': temp_files,
            'count': len(temp_files),
            'total_size': total_size,
            'total_size_formatted': format_bytes(total_size),
        }
    
    def scan_browser_cache(self, progress_callback: Callable = None) -> Dict:
        """Scan browser cache directories"""
        cache_files = []
        total_size = 0
        
        browser_caches = get_browser_cache_paths()
        
        for browser, cache_path in browser_caches.items():
            if progress_callback:
                progress_callback(f"Scanning {browser} cache...")
            
            try:
                # Calculate cache directory size
                cache_size = calculate_directory_size(cache_path)
                
                if cache_size > 0:
                    cache_files.append({
                        'path': cache_path,
                        'size': cache_size,
                        'size_formatted': format_bytes(cache_size),
                        'category': f'{browser} Cache',
                        'location': cache_path,
                        'is_directory': True,
                    })
                    total_size += cache_size
            
            except Exception as e:
                print(f"Error scanning {browser} cache: {e}")
        
        return {
            'files': cache_files,
            'count': len(cache_files),
            'total_size': total_size,
            'total_size_formatted': format_bytes(total_size),
        }
    
    def scan_recycle_bin(self, progress_callback: Callable = None) -> Dict:
        """Scan Windows Recycle Bin"""
        recycle_bin_size = 0
        
        if progress_callback:
            progress_callback("Scanning Recycle Bin...")
        
        try:
            # Windows Recycle Bin path
            recycle_bin = r'C:\$Recycle.Bin'
            if os.path.exists(recycle_bin):
                recycle_bin_size = calculate_directory_size(recycle_bin)
        except Exception as e:
            print(f"Error scanning Recycle Bin: {e}")
        
        return {
            'size': recycle_bin_size,
            'size_formatted': format_bytes(recycle_bin_size),
        }
    
    def perform_full_scan(self, progress_callback: Callable = None) -> Dict:
        """Perform a full system scan"""
        self.is_scanning = True
        self.scan_results = {
            'temp_files': [],
            'browser_cache': [],
            'recycle_bin': {},
        }
        
        # Scan temporary files
        if progress_callback:
            progress_callback("Scanning temporary files...")
        temp_results = self.scan_temp_files(progress_callback)
        self.scan_results['temp_files'] = temp_results['files']
        
        # Scan browser cache
        if progress_callback:
            progress_callback("Scanning browser cache...")
        cache_results = self.scan_browser_cache(progress_callback)
        self.scan_results['browser_cache'] = cache_results['files']
        
        # Scan recycle bin
        recycle_results = self.scan_recycle_bin(progress_callback)
        self.scan_results['recycle_bin'] = recycle_results
        
        # Calculate total
        self.total_size = (
            temp_results['total_size'] + 
            cache_results['total_size'] + 
            recycle_results['size']
        )
        
        self.is_scanning = False
        
        if progress_callback:
            progress_callback("Scan complete!")
        
        return {
            'temp_files': temp_results,
            'browser_cache': cache_results,
            'recycle_bin': recycle_results,
            'total_size': self.total_size,
            'total_size_formatted': format_bytes(self.total_size),
            'total_items': temp_results['count'] + cache_results['count'],
        }
    
    def clean_selected_files(self, file_paths: List[str], 
                           progress_callback: Callable = None) -> Dict:
        """Delete selected files"""
        deleted_count = 0
        failed_count = 0
        freed_space = 0
        errors = []
        
        for filepath in file_paths:
            if progress_callback:
                progress_callback(f"Deleting: {os.path.basename(filepath)}")
            
            try:
                # Get file size before deletion
                size = os.path.getsize(filepath) if os.path.isfile(filepath) else 0
                
                # Delete file or directory
                if os.path.isfile(filepath):
                    success, message = safe_delete_file(filepath)
                elif os.path.isdir(filepath):
                    import shutil
                    shutil.rmtree(filepath)
                    success = True
                
                if success:
                    deleted_count += 1
                    freed_space += size
                else:
                    failed_count += 1
                    errors.append(f"{filepath}: {message}")
            
            except Exception as e:
                failed_count += 1
                errors.append(f"{filepath}: {str(e)}")
        
        return {
            'deleted_count': deleted_count,
            'failed_count': failed_count,
            'freed_space': freed_space,
            'freed_space_formatted': format_bytes(freed_space),
            'errors': errors,
        }
    
    def empty_recycle_bin(self) -> Tuple[bool, str]:
        """Empty the Windows Recycle Bin"""
        try:
            import ctypes
            ctypes.windll.shell32.SHEmptyRecycleBinW(None, None, 0)
            return True, "Recycle Bin emptied successfully"
        except Exception as e:
            return False, f"Error emptying Recycle Bin: {str(e)}"
