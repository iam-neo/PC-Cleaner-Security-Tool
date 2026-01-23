"""
Malware Scanner Module - Scans for and removes malware
"""
import os
import re
import hashlib
import psutil
import json
from typing import List, Dict, Callable, Tuple
from pathlib import Path
from utils.file_operations import get_file_hash, move_to_quarantine, scan_directory_for_files
from utils.system_info import get_running_processes, format_bytes
import config


class MalwareScanner:
    def __init__(self):
        self.scan_results = []
        self.is_scanning = False
        self.threats_found = 0
        self.files_scanned = 0
        
        # Load malware signatures
        self.malware_signatures = self._load_malware_signatures()
        
    def _load_malware_signatures(self) -> Dict:
        """Load malware signatures from database"""
        signatures_file = config.RESOURCES_DIR / "malware_signatures.json"
        
        # Create default signatures if file doesn't exist
        if not signatures_file.exists():
            default_signatures = {
                "hashes": {
                    # Example malware hashes (these are fake examples)
                    "d41d8cd98f00b204e9800998ecf8427e": "Generic.Trojan",
                },
                "patterns": [
                    r".*\.exe\.exe$",  # Double extension
                    r".*\.scr$",       # Screensaver files (often malware)
                    r".*\.pif$",       # Program Information File
                ],
                "suspicious_names": [
                    "svchost.exe",  # If not in System32
                    "csrss.exe",    # If not in System32
                    "winlogon.exe", # If not in System32
                ]
            }
            
            with open(signatures_file, 'w') as f:
                json.dump(default_signatures, f, indent=2)
            
            return default_signatures
        
        try:
            with open(signatures_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading signatures: {e}")
            return {"hashes": {}, "patterns": [], "suspicious_names": []}
    
    def scan_file(self, filepath: str) -> Dict:
        """
        Scan a single file for malware
        Returns: Dict with threat info or None if clean
        """
        threats = []
        
        try:
            # Skip if file is too large
            file_size = os.path.getsize(filepath)
            if file_size > config.MAX_FILE_SIZE_MB * 1024 * 1024:
                return None
            
            filename = os.path.basename(filepath)
            
            # Check 1: Pattern matching
            for pattern in self.malware_signatures.get('patterns', []):
                if re.match(pattern, filename, re.IGNORECASE):
                    threats.append({
                        'type': 'Suspicious Pattern',
                        'description': f'Filename matches malware pattern: {pattern}',
                        'severity': 'Medium',
                    })
            
            # Check 2: Suspicious file names in wrong locations
            for suspicious_name in self.malware_signatures.get('suspicious_names', []):
                if filename.lower() == suspicious_name.lower():
                    # Check if it's in the correct system directory
                    if not filepath.lower().startswith(r'c:\windows\system32'):
                        threats.append({
                            'type': 'Suspicious Location',
                            'description': f'System file "{suspicious_name}" found outside System32',
                            'severity': 'High',
                        })
            
            # Check 3: Hash-based detection (for executable files)
            if filepath.lower().endswith(('.exe', '.dll', '.scr', '.bat', '.cmd')):
                file_hash = get_file_hash(filepath, 'md5')
                if file_hash in self.malware_signatures.get('hashes', {}):
                    malware_name = self.malware_signatures['hashes'][file_hash]
                    threats.append({
                        'type': 'Known Malware',
                        'description': f'File matches known malware: {malware_name}',
                        'severity': 'Critical',
                    })
            
            # Check 4: Hidden executable files
            if filepath.lower().endswith(('.exe', '.bat', '.cmd', '.scr')):
                try:
                    import ctypes
                    attrs = ctypes.windll.kernel32.GetFileAttributesW(filepath)
                    if attrs != -1 and (attrs & 2):  # FILE_ATTRIBUTE_HIDDEN
                        threats.append({
                            'type': 'Hidden Executable',
                            'description': 'Executable file with hidden attribute',
                            'severity': 'Medium',
                        })
                except:
                    pass
            
            if threats:
                return {
                    'path': filepath,
                    'filename': filename,
                    'size': file_size,
                    'size_formatted': format_bytes(file_size),
                    'threats': threats,
                    'threat_count': len(threats),
                    'max_severity': self._get_max_severity(threats),
                }
            
        except Exception as e:
            print(f"Error scanning {filepath}: {e}")
        
        return None
    
    def _get_max_severity(self, threats: List[Dict]) -> str:
        """Get the maximum severity level from a list of threats"""
        severity_order = {'Low': 1, 'Medium': 2, 'High': 3, 'Critical': 4}
        max_severity = 'Low'
        
        for threat in threats:
            if severity_order.get(threat['severity'], 0) > severity_order.get(max_severity, 0):
                max_severity = threat['severity']
        
        return max_severity
    
    def scan_directory(self, directory: str, progress_callback: Callable = None) -> List[Dict]:
        """Scan a directory for malware"""
        threats = []
        files_scanned = 0
        
        try:
            # Get all executable and script files
            extensions = ['.exe', '.dll', '.scr', '.bat', '.cmd', '.vbs', '.js', '.jar']
            files = scan_directory_for_files(directory, extensions)
            
            for filepath in files:
                if progress_callback:
                    progress_callback(f"Scanning: {os.path.basename(filepath)}")
                
                result = self.scan_file(filepath)
                if result:
                    threats.append(result)
                
                files_scanned += 1
        
        except Exception as e:
            print(f"Error scanning directory {directory}: {e}")
        
        return threats
    
    def perform_quick_scan(self, progress_callback: Callable = None) -> Dict:
        """Perform a quick scan of common malware locations"""
        self.is_scanning = True
        self.scan_results = []
        self.files_scanned = 0
        
        # Common malware locations
        scan_locations = [
            os.environ.get('TEMP', ''),
            os.environ.get('APPDATA', ''),
            os.path.join(os.environ.get('USERPROFILE', ''), 'Downloads'),
        ]
        
        for location in scan_locations:
            if location and os.path.exists(location):
                if progress_callback:
                    progress_callback(f"Scanning: {location}")
                
                threats = self.scan_directory(location, progress_callback)
                self.scan_results.extend(threats)
        
        self.threats_found = len(self.scan_results)
        self.is_scanning = False
        
        return {
            'threats': self.scan_results,
            'threat_count': self.threats_found,
            'files_scanned': self.files_scanned,
        }
    
    def perform_full_scan(self, progress_callback: Callable = None) -> Dict:
        """Perform a full system scan"""
        self.is_scanning = True
        self.scan_results = []
        self.files_scanned = 0
        
        # Scan entire C: drive
        if progress_callback:
            progress_callback("Performing full system scan...")
        
        threats = self.scan_directory('C:\\', progress_callback)
        self.scan_results.extend(threats)
        
        self.threats_found = len(self.scan_results)
        self.is_scanning = False
        
        return {
            'threats': self.scan_results,
            'threat_count': self.threats_found,
            'files_scanned': self.files_scanned,
        }
    
    def scan_running_processes(self) -> List[Dict]:
        """Scan running processes for suspicious activity"""
        suspicious_processes = []
        
        processes = get_running_processes()
        
        for proc in processes:
            # Check for suspicious process names
            for suspicious_name in self.malware_signatures.get('suspicious_names', []):
                if proc['name'].lower() == suspicious_name.lower():
                    # Additional check: verify it's running from correct location
                    try:
                        process = psutil.Process(proc['pid'])
                        exe_path = process.exe()
                        
                        if not exe_path.lower().startswith(r'c:\windows\system32'):
                            suspicious_processes.append({
                                'pid': proc['pid'],
                                'name': proc['name'],
                                'path': exe_path,
                                'reason': 'System process running from suspicious location',
                                'severity': 'High',
                            })
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        pass
        
        return suspicious_processes
    
    def quarantine_threat(self, filepath: str) -> Tuple[bool, str]:
        """Move a threat to quarantine"""
        return move_to_quarantine(filepath)
    
    def remove_threat(self, filepath: str) -> Tuple[bool, str]:
        """Permanently delete a threat"""
        try:
            os.remove(filepath)
            return True, "Threat removed successfully"
        except Exception as e:
            return False, f"Error removing threat: {str(e)}"
    
    def terminate_process(self, pid: int) -> Tuple[bool, str]:
        """Terminate a suspicious process"""
        try:
            process = psutil.Process(pid)
            process.terminate()
            process.wait(timeout=3)
            return True, f"Process {pid} terminated successfully"
        except psutil.NoSuchProcess:
            return False, "Process not found"
        except psutil.AccessDenied:
            return False, "Access denied - requires administrator privileges"
        except Exception as e:
            return False, f"Error: {str(e)}"
