"""
Windows Security Hardening Module

Purpose:
This module provides functionality to audit, verify, and harden the security posture
of the Windows operating system. It is designed to be modular and safe.

Key Principles:
1.  **Windows Only**: This module detects non-Windows environments and does not run.
2.  **Explicit Consent**: All security changes (hardening) must be explicitly requested by the user.
3.  **Optional**: No changes are applied automatically.
4.  **Safe**: Remediation supports dry-run modes and checks for necessary privileges.

Structure:
- Audit: startup items, registry keys.
- Verification: digital signature checks (Sigcheck/Fallback).
- Posture: Firewall, UAC, Windows Defender status.
- Hardening: Remediation functions.
"""

import os
import shutil
import subprocess
from typing import List, Dict, Optional
from utils.system_info import ensure_windows_os

class SecurityHardener:
    """
    Main class for Security Hardening operations.
    """
    def __init__(self):
        """
        Initialize the Security Hardener.
        """
        self.check_os()
        self.sigcheck_path = self._find_sigcheck()

    def _find_sigcheck(self) -> Optional[str]:
        """Find sigcheck.exe in PATH or common locations"""
        return shutil.which("sigcheck.exe") or shutil.which("sigcheck")

    def check_os(self):
        """
        Check if the current OS is Windows.
        """
        return ensure_windows_os(raise_exception=False)

    # ==========================================
    # Security Audit Functions
    # ==========================================
    def audit_startup(self) -> List[Dict]:
        """
        Audit startup locations (Startup folders + Registry Run keys).
        Returns a list of dicts with file info and signature status.
        """
        if not self.check_os():
            return []

        items = []
        try:
            import winreg
            
            # 1. Registry Run Keys
            registry_paths = [
                (winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\Run"),
                (winreg.HKEY_LOCAL_MACHINE, r"Software\WOW6432Node\Microsoft\Windows\CurrentVersion\Run"),
                (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run"),
            ]

            for root, path in registry_paths:
                try:
                    with winreg.OpenKey(root, path, 0, winreg.KEY_READ) as key:
                        i = 0
                        while True:
                            try:
                                name, value, _ = winreg.EnumValue(key, i)
                                items.append({
                                    "location": "Registry",
                                    "path": path,
                                    "name": name,
                                    "command": value,
                                    "root": "HKLM" if root == winreg.HKEY_LOCAL_MACHINE else "HKCU"
                                })
                                i += 1
                            except OSError:
                                break
                except OSError:
                    continue 

            # 2. Startup Folders
            startup_dirs = [
                os.path.join(os.getenv("APPDATA", ""), r"Microsoft\Windows\Start Menu\Programs\Startup"),
                os.path.join(os.getenv("PROGRAMDATA", ""), r"Microsoft\Windows\Start Menu\Programs\Startup")
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

            # Check signatures
            for item in items:
                # Extract clean path from command
                cmd = item["command"]
                exe_path = cmd
                if cmd.startswith('"'):
                    exe_path = cmd.split('"')[1]
                elif " " in cmd and not os.path.exists(cmd):
                    # Simple heuristic for unquoted paths with args
                    exe_path = cmd.split(" ")[0]
                
                # Check for existence before verifying
                if not os.path.exists(exe_path) and os.path.exists(cmd):
                     exe_path = cmd
                     
                sig_info = self._verify_signature(exe_path)
                item.update(sig_info)
                
            return items

        except Exception as e:
            print(f"Audit failed: {e}")
            return []

    # ==========================================
    # Digital Signature Verification
    # ==========================================
    def _verify_signature(self, filepath: str) -> Dict:
        """
        Check digital signature for a specific file.
        Uses sigcheck if available, else falls back to basic existence check.
        """
        result = {
            "path": filepath,
            "signed": False,
            "verified": False,
            "publisher": "Unknown",
            "method": "fallback"
        }
        
        if not filepath or not os.path.exists(filepath):
            result["publisher"] = "File not found"
            return result

        # Method 1: Sigcheck (Preferred)
        if self.sigcheck_path:
            try:
                # -a: extended info, -q: quiet, -v: csv output (simplifies parsing)
                cmd = [self.sigcheck_path, "-a", "-q", "-v", filepath]
                proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
                output = proc.stdout
                
                # Check verification string
                if "Verified:\tSigned" in output or "Verified:	Signed" in output:
                     result["signed"] = True
                     result["verified"] = True
                     result["method"] = "sigcheck"
                     
                     # Extract publisher
                     for line in output.splitlines():
                         if line.startswith("Publisher:"):
                             result["publisher"] = line.split(":", 1)[1].strip()
                             break # Found valid publisher
                elif "Verified" in output:
                    # Capture unverified state explicitly if needed
                    pass
                    
                return result
            except Exception:
                pass # Fall through to fallback

        # Method 2: Fallback (Basic)
        # Without external libs like pefile/pywin32, we can't reliably verify signatures.
        # We mark as "Unknown" but acknowledge file exists.
        result["publisher"] = "Unverifiable (Missing sigcheck)"
        result["method"] = "none"
        
        return result

    # ==========================================
    # System Posture Checks
    # ==========================================
    def check_posture(self):
        """
        Check current system security posture (Firewall, UAC, Defender).
        Returns a dictionary: { "Check Name": (current_state, recommended_state, needs_fix_bool) }
        """
        if not self.check_os():
            return {}

        results = {}
        
        # 1. Windows Firewall
        results["Windows Firewall"] = self._audit_firewall()
            
        # 2. User Account Control (UAC)
        results["UAC"] = self._audit_uac()

        # 3. Windows Defender
        results["Windows Defender"] = self._audit_defender()

        return results

    def _audit_firewall(self):
        """Check Windows Firewall status (Standard Profile)"""
        try:
            import subprocess
            # 'netsh advfirewall show allprofiles state' is a good check
            cmd = ["netsh", "advfirewall", "show", "allprofiles", "state"]
            # Use specific encoding/errors to avoid issues on some non-English systems if possible, 
            # but standard creates simple text output "State ON"
            proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
            output = proc.stdout
            
            if "State" in output and "ON" in output:
                # Naive check: if we see "State ON", at least one profile is ON.
                # Ideally we want all to be on.
                # If we see "OFF", it might be bad.
                if "OFF" in output:
                     return ("Partial/Off", "On", True)
                return ("On", "On", False)
            else:
                return ("Unknown/Off", "On", True)
        except Exception as e:
            return (f"Error: {str(e)}", "On", True)

    def _audit_uac(self):
        """Check UAC Level via Registry"""
        try:
            import winreg
            key_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System"
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path) as key:
                enable_lua, _ = winreg.QueryValueEx(key, "EnableLUA")
                # EnableLUA=1 means UAC is on. =0 means off.
                
                # Check ConsentPromptBehaviorAdmin for stricter levels?
                # For basic check, EnableLUA is sufficient.
                current = "Enabled" if enable_lua == 1 else "Disabled"
                return (current, "Enabled", enable_lua == 0)
        except WindowsError:
            return ("Unknown (Access Denied?)", "Enabled", True)
        except Exception as e:
            return (f"Error: {str(e)}", "Enabled", True)

    def _audit_defender(self):
        """Check Windows Defender Real-Time Protection"""
        try:
            import subprocess
            # Get-MpComputerStatus is robust but requires PowerShell
            cmd = ["powershell", "-Command", "Get-MpComputerStatus | Select-Object -ExpandProperty RealTimeProtectionEnabled"]
            proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
            output = proc.stdout.strip()
            
            if output.lower() == "true":
                return ("Active", "Active", False)
            elif output.lower() == "false":
                return ("Inactive", "Active", True)
            else:
                 # Fallback check methods if PS fails or custom AV exists?
                 return ("Unknown", "Active", True)
        except Exception as e:
            return (f"Error: {str(e)}", "Active", True)

    # ==========================================
    # Safe Remediation Layer
    # ==========================================
    def apply_security_best_practices(self, dry_run: bool = True) -> List[str]:
        """
        Apply security hardening changes.
        
        Args:
            dry_run (bool): If True, simulate changes only.
            
        Returns:
            List[str]: Log of actions taken.
        """
        logs = []
        if not self.check_os():
            return ["Skipped: Non-Windows OS"]

        # 1. Check Admin Privileges
        try:
            import ctypes
            is_admin = ctypes.windll.shell32.IsUserAnAdmin()
        except:
            is_admin = False
             
        if not is_admin and not dry_run:
            return ["Failed: Administrator privileges required to apply changes."]

        # 2. Check current posture to avoid blind toggling
        posture = self.check_posture()
        
        # 3. Define Remediation Actions
        # Format: (CheckName, DesiredState, ActionName, ActionFunc)
        uac_current, _, uac_needs_fix = posture.get("UAC", ("Unknown", "Enabled", False))
        fw_current, _, fw_needs_fix = posture.get("Windows Firewall", ("Unknown", "On", False))
        
        actions_to_take = []
        
        if uac_needs_fix:
            actions_to_take.append(("UAC", "Enabled", "Enable UAC", self._enable_uac))
        
        if fw_needs_fix:
             actions_to_take.append(("Firewall", "On", "Enable Firewall", self._enable_firewall))

        if not actions_to_take:
            return ["System is already hardened. No changes needed."]

        # 4. Execute Actions
        for system, target, name, func in actions_to_take:
            if dry_run:
                logs.append(f"[DRY RUN] Would execute: {name} (Current: {posture.get(system)[0]})")
            else:
                try:
                    result = func()
                    logs.append(f"[SUCCESS] {name}: {result}")
                except Exception as e:
                    logs.append(f"[ERROR] Failed to {name}: {str(e)}")
                    
        return logs

    def _enable_uac(self) -> str:
        """Enable UAC via Registry (Requires Admin)"""
        import winreg
        try:
            key_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System"
            # Open key with write access
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_SET_VALUE) as key:
                winreg.SetValueEx(key, "EnableLUA", 0, winreg.REG_DWORD, 1)
            return "UAC Enabled. Reboot required for full effect."
        except Exception as e:
            raise e

    def _enable_firewall(self) -> str:
        """Enable Firewall via netsh (Requires Admin)"""
        # netsh advfirewall set allprofiles state on
        cmd = ["netsh", "advfirewall", "set", "allprofiles", "state", "on"]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return "Windows Firewall enabled for all profiles."
