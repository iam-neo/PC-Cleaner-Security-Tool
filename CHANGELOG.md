# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-01-28

### Added
- **Windows Security Hardening Module**: A new module to audit and improve system security details.
    - **Startup Audit**: Scans Registry Run keys and Startup folders for unsigned or suspicious executables.
    - **Digital Signature Verification**: Automatically uses `sigcheck.exe` (if available) to verify file signatures.
    - **System Posture Checks**: read-only audits for Windows Firewall, UAC status, and Windows Defender Real-Time Protection.
    - **Safe Remediation**: `apply_security_best_practices()` function to enable UAC and Firewall (requires Admin).
- **Security Tab**: A new UI tab in the main application for the Security Module.
- **CLI Tool**: `security_check.py` for running security audits and checks from the command line with rich output.
- **Windows Guard**: `ensure_windows_os` utility to prevent execution on non-Windows platforms.
- `utils/cli_renderer.py` for formatted console output.

### Changed
- Updated `requirements.txt` to include `rich` library.
- Refactored `pc_cleaner_app.py` to integrate the new Security Tab.
