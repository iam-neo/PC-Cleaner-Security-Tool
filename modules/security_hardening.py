"""
Windows Security Hardening Module
"""
import os
import sys
import platform
import subprocess
import logging
import ctypes
import shutil
from typing import List, Dict, Tuple, Optional
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Constants
STARTUP_REGISTRY_KEYS = [
    r"Software\Microsoft\Windows\CurrentVersion\Run",
    r"Software\Microsoft\Windows\CurrentVersion\RunOnce",
    r"Software\WOW6432Node\Microsoft\Windows\CurrentVersion\Run",
    r"Software\WOW6432Node\Microsoft\Windows\CurrentVersion\RunOnce",
]

class SecurityHardener:
    def __init__(self):
        self.is_windows = platform.system() == "Windows"
        self.sigcheck_path = self._find_sigcheck()
        
    def _find_sigcheck(self) -> Optional[str]:
        """Find sigcheck.exe in PATH or common locations"""
        return shutil.which("sigcheck.exe") or shutil.which("sigcheck")

    def check_os(self) -> bool:
        """Verify if running on Windows"""
        if not self.is_windows:
            logger.warning("Security Hardening Module is only supported on Windows.")
            return False
        return True

    def _verify_signature(self, filepath: str) -> Dict:
        """
        Verify digital signature of a file.
        Uses sigcheck if available, else falls back to rudimentary checks.
        """
        result = {
            "path": filepath,
            "signed": False,
            "verified": False,
            "publisher": "Unknown",
            "method": "fallback"
        }
        
        if not os.path.exists(filepath):
            result["error"] = "File not found"
            return result

        # Method 1: Sysinternals Sigcheck (Preferred)
        if self.sigcheck_path:
            try:
                # -a: extended info, -h: hashes, -v: csv output, -q: quiet
                cmd = [self.sigcheck_path, "-a", "-q", "-v", filepath]
                # Note: parsing CSV output from sigcheck can be tricky reliably without a full CSV parser,
                # but let's try a simpler approach or just check exit code for verification?
                # Actually, sigcheck prints info. Let's return basic 'verified' if string "Verified" is in output?
                # Better: Check for "Verified:	Signed" string in output.
                
                proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
                output = proc.stdout
                
                if "Verified:\tSigned" in output or "Verified:	Signed" in output:
                     result["signed"] = True
                     result["verified"] = True
                     result["method"] = "sigcheck"
                     
                     # Extract publisher
                     for line in output.splitlines():
                         if line.strip().startswith("Publisher:"):
                             result["publisher"] = line.split(":", 1)[1].strip().strip("\t")
                             break
                return result
            except Exception as e:
                logger.error(f"Sigcheck failed for {filepath}: {e}")

        # Method 2: WinVerifyTrust (Fallback via ctypes)
        # This is complex to implement fully in Python without pywin32.
        # We will use a simplified check or skip if dependencies are strict.
        # For now, let's mark as 'Unknown/Unchecked' if sigcheck missing, 
        # or we could try to read PE headers if we had `pefile`.
        # Since we want to avoid side-effects/heavy deps, we will return 'Unknown'
        # but with a note.
        
        result["note"] = "Sigcheck not found. Signature verification skipped."
        return result

    def audit_startup(self) -> List[Dict]:
        """Audit startup items from Registry and Startup folder"""
        if not self.is_windows:
            return []
            
        import winreg
        items = []

        # 1. Registry
        for key_path in STARTUP_REGISTRY_KEYS:
            for root_key in [winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_CURRENT_USER]:
                try:
                    with winreg.OpenKey(root_key, key_path, 0, winreg.KEY_READ) as key:
                        i = 0
                        while True:
                            try:
                                name, value, _ = winreg.EnumValue(key, i)
                                items.append({
                                    "location": "Registry",
                                    "path": key_path,
                                    "name": name,
                                    "command": value,
                                    "root": "HKLM" if root_key == winreg.HKEY_LOCAL_MACHINE else "HKCU"
                                })
                                i += 1
                            except OSError:
                                break
                except OSError:
                    continue  # Key likely doesn't exist

        # 2. Startup Folder
        startup_dirs = [
             os.path.join(os.getenv("APPDATA"), r"Microsoft\Windows\Start Menu\Programs\Startup"),
             os.path.join(os.getenv("PROGRAMDATA"), r"Microsoft\Windows\Start Menu\Programs\Startup")
        ]
        
        for folder in startup_dirs:
            if os.path.exists(folder):
                for file in os.listdir(folder):
                     full_path = os.path.join(folder, file)
                     if os.path.isfile(full_path):
                         items.append({
                             "location": "Startup Folder",
                             "path": folder,
                             "name": file,
                             "command": full_path,
                             "root": "FileSystem"
                         })

        # Enrich with signature check
        for item in items:
            # Extract executable path from command string (naive)
            cmd = item["command"]
            if cmd.startswith('"'):
                exe_path = cmd.split('"')[1]
            else:
                exe_path = cmd.split(" ")[0]
            
            # Verify if it's an exe and exists
            if not os.path.exists(exe_path) and os.path.exists(cmd):
                exe_path = cmd
            
            sig_info = self._verify_signature(exe_path)
            item.update(sig_info)

        return items

    def check_posture(self) -> Dict[str, Tuple[str, str, bool]]:
        """
        Check system security posture.
        Returns Dict: { CheckName: (Current, Recommended, NeedsFix) }
        """
        if not self.is_windows:
             return {}
             
        posture = {}
        
        # 1. UAC Check
        try:
             import winreg
             with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System") as key:
                 enable_lua, _ = winreg.QueryValueEx(key, "EnableLUA")
                 # 1 is Enabled, 0 is Disabled
                 current = "Enabled" if enable_lua == 1 else "Disabled"
                 posture["UAC"] = (current, "Enabled", enable_lua == 0)
        except Exception as e:
            posture["UAC"] = ("Error", "Enabled", True)
            
        # 2. Firewall Check (via netsh)
        try:
            # Check all profiles
            proc = subprocess.run(["netsh", "advfirewall", "show", "allprofiles", "state"], capture_output=True, text=True)
            if "State                                 ON" in proc.stdout:
                 current = "On"
                 needs_fix = False
            else:
                 current = "Off/Partial"
                 needs_fix = True
            
            posture["Firewall"] = (current, "On", needs_fix)
        except Exception:
             posture["Firewall"] = ("Unknown", "On", True)

        # 3. Windows Defender (via PowerShell - Get-MpComputerStatus)
        try:
             # Basic check if service is running
             import psutil
             defender_running = "MsMpEng.exe" in (p.name() for p in psutil.process_iter(['name']))
             current = "Running" if defender_running else "Stopped/Missing"
             posture["Windows Defender"] = (current, "Running", not defender_running)
        except Exception:
             posture["Windows Defender"] = ("Unknown", "Running", True)

        return posture

    def apply_security_best_practices(self, dry_run: bool = True) -> List[str]:
        """
        Apply security best practices.
        """
        logs = []
        if not self.is_windows:
            return ["Skipped: Non-Windows OS"]

        # Check Admin
        try:
             is_admin = ctypes.windll.shell32.IsUserAnAdmin()
        except:
             is_admin = False
             
        if not is_admin:
            return ["Failed: Administrator privileges required to apply changes."]

        actions = [
            ("Enable UAC", self._enable_uac),
            ("Enable Firewall", self._enable_firewall)
        ]
        
        for name, func in actions:
            try:
                if dry_run:
                    logs.append(f"[DRY RUN] Would execute: {name}")
                else:
                    result = func()
                    logs.append(f"Executed {name}: {result}")
            except Exception as e:
                logs.append(f"Error executing {name}: {e}")
                
        return logs

    def _enable_uac(self) -> str:
        """Enable UAC via Registry"""
        import winreg
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System", 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, "EnableLUA", 0, winreg.REG_DWORD, 1)
            winreg.CloseKey(key)
            return "Success (Reboot required)"
        except Exception as e:
            raise e

    def _enable_firewall(self) -> str:
        """Enable Firewall via netsh"""
        subprocess.run(["netsh", "advfirewall", "set", "allprofiles", "state", "on"], check=True)
        return "Success"

if __name__ == "__main__":
    # CLI Check
    hardener = SecurityHardener()
    if hardener.check_os():
        print("Auditing Startup Items...")
        items = hardener.audit_startup()
        for item in items:
            print(item)
            
        print("\nChecking Posture...")
        posture = hardener.check_posture()
        for k, v in posture.items():
            print(f"{k}: {v}")
