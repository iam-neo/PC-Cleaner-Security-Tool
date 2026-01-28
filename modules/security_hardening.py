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

    def check_os(self):
        """
        Check if the current OS is Windows.
        """
        return ensure_windows_os(raise_exception=False)

    # ==========================================
    # TODO: Security Audit Functions
    # ==========================================
    def audit_startup(self):
        """
        Audit startup locations (Startup folders + Registry Run keys).
        TODO: Implement registry and file system checks.
        """
        pass

    # ==========================================
    # TODO: Digital Signature Verification
    # ==========================================
    def _verify_signature(self, filepath):
        """
        Check digital signature for a specific file.
        TODO: Implement sigcheck.exe wrapper or fallback logic.
        """
        pass

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
    # TODO: Safe Remediation Layer
    # ==========================================
    def apply_security_best_practices(self, dry_run=True):
        """
        Apply security hardening changes.
        
        Args:
            dry_run (bool): If True, simulate changes only.
            
        TODO: Implement hardening logic with admin check.
        """
        pass
