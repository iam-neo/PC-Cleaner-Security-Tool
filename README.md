# 🛡️ PC Cleaner & Security Tool

A powerful Windows desktop application to clean temporary files, cache, and scan for malware on your PC.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey)

## ✨ Features

### PC Cleaner
- 🧹 **Clean Temporary Files** - Remove system temp files and free up disk space
- 🌐 **Browser Cache Cleaning** - Clear cache from Chrome, Edge, Firefox, and Opera
- 🗑️ **Empty Recycle Bin** - Permanently delete files from Recycle Bin
- 📊 **Detailed Scan Results** - See exactly what will be deleted before cleaning
- ✅ **Safe Deletion** - Protected system paths are never touched

### Malware Scanner
- 🔍 **Quick & Full Scans** - Choose between quick scan or comprehensive system scan
- 🛡️ **Pattern-Based Detection** - Identify suspicious file patterns and behaviors
- 🔐 **Hash-Based Detection** - Detect known malware using signature database
- ⚙️ **Process Monitoring** - Scan running processes for suspicious activity
- 🔒 **Quarantine System** - Safely isolate threats before deletion
- 🗑️ **Threat Removal** - Permanently delete detected malware

### Windows Security Hardening (New!)
- 🛡️ **System Posture Check** - Audit Windows Firewall, UAC, and Defender status
- 🚦 **Startup Audit** - Detect unsigned applications in Startup and Registry
- 🔒 **Safe Remediation** - Enable essential security features (Admin only)
- 📝 **Digital Signature Verification** - Verify publisher identities (uses Sysinternals Sigcheck)
- ⚠️ **Zero-Risk** - No files are automatically deleted; changes require explicit user confirmation.

### Dashboard
- 💻 **System Information** - View OS, processor, and system details
- 💾 **Disk Usage Monitoring** - Real-time disk space statistics
- ⚡ **Quick Actions** - One-click access to common tasks
- 📊 **Scan History** - Track your last scan results

## 🚀 Installation

### Prerequisites
- Windows 10 or later
- Python 3.8 or higher

### Setup

1. **Clone or download this repository**
   ```bash
   cd C:\xampp\htdocs\pro
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python pc_cleaner_app.py
   ```

### Running as Administrator (Recommended)

For full functionality, run the application with administrator privileges:

1. Right-click on `pc_cleaner_app.py`
2. Select "Run as administrator"

Or use PowerShell:
```powershell
Start-Process python -ArgumentList "pc_cleaner_app.py" -Verb RunAs
```

## 📦 Building Standalone Executable

To create a standalone `.exe` file that can run without Python installed:

```bash
python build.py
```

The executable will be created in the `dist` folder.

## 🎯 Usage Guide

### PC Cleaner

1. Navigate to the **PC Cleaner** tab
2. Click **Start Scan** to scan for temporary files and cache
3. Review the scan results - files are selected by default
4. Uncheck any files you want to keep
5. Click **Clean Selected** to delete the files
6. Confirm the deletion by typing "YES"

### Malware Scanner

1. Navigate to the **Malware Scanner** tab
2. Choose scan type:
   - **Quick Scan** - Scans common malware locations (faster)
   - **Full Scan** - Scans entire system (thorough)
   - **Scan Processes** - Checks running processes
3. Review detected threats
4. For each threat, you can:
   - **Quarantine** - Move to quarantine folder
   - **Delete** - Permanently remove
   - **Ignore** - Skip this detection

### Dashboard

- View system information and disk usage
- Use **Quick Clean** to jump to PC Cleaner
- Use **Quick Scan** to jump to Malware Scanner
- Click **Refresh Dashboard** to update statistics

### Security Hardening CLI
Run the security audit from the command line:
```bash
# Check system status
python security_check.py --posture

# Audit startup items
python security_check.py --audit

# Dry-run hardening (simulate changes)
python security_check.py --apply --dry-run
```

## ⚙️ Configuration

Edit `config.py` to customize:

- Scan paths and directories
- Protected system paths
- UI theme (dark/light)
- File extensions to scan
- Maximum file size for scanning
- VirusTotal API integration (optional)

## 🔒 Safety Features

- **Protected Paths** - System-critical directories are never scanned or deleted
- **Confirmation Dialogs** - All destructive actions require explicit confirmation
- **Quarantine System** - Suspicious files can be isolated instead of deleted
- **Detailed Logging** - All actions are logged for review

## ⚠️ Important Notes

### Malware Detection Limitations

This tool provides **basic malware detection** and is **NOT** a replacement for professional antivirus software like Windows Defender. It uses:

- Pattern matching for suspicious file names
- Hash-based detection for known malware
- Behavioral analysis for running processes

For comprehensive protection, always use a full-featured antivirus solution.

### Administrator Privileges

Some features require administrator privileges:
- Accessing system temp directories
- Deleting protected files
- Terminating system processes
- Emptying Recycle Bin

The application will warn you if not running as administrator.

## 📁 Project Structure

```
pro/
├── pc_cleaner_app.py       # Main application entry point
├── config.py               # Configuration settings
├── requirements.txt        # Python dependencies
├── build.py               # Build script for .exe
├── modules/
│   ├── cleaner.py         # PC cleaning logic
│   └── scanner.py         # Malware scanning logic
├── ui/
│   ├── dashboard.py       # Dashboard UI
│   ├── cleaner_tab.py     # PC Cleaner UI
│   ├── scanner_tab.py     # Malware Scanner UI
│   └── security_tab.py    # Security Hardening UI
├── utils/
│   ├── cli_renderer.py    # CLI formatting helpers
│   ├── file_operations.py # File handling utilities
│   └── system_info.py     # System information utilities
├── resources/
│   └── malware_signatures.json  # Malware signature database
├── logs/                  # Application logs
└── quarantine/           # Quarantined files
```

## 🛠️ Troubleshooting

### "Permission Denied" Errors
- Run the application as administrator
- Check that files are not in use by other programs

### Scan Takes Too Long
- Use Quick Scan instead of Full Scan
- Adjust `MAX_FILE_SIZE_MB` in config.py

### False Positives in Malware Scanner
- Review the threat details carefully
- Use "Ignore" for known safe files
- Update malware signatures in `resources/malware_signatures.json`

## 📝 License

This project is provided as-is for educational and personal use.

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Improve malware signature database

## ⚡ Performance Tips

- Close other applications before running Full Scan
- Run scans during low-activity periods
- Regularly clean temp files to maintain performance
- Keep malware signatures updated

## 🔄 Updates

To update the malware signature database:
1. Edit `resources/malware_signatures.json`
2. Add new malware hashes and patterns
3. Restart the application

## 📞 Support

For issues or questions:
1. Check the Troubleshooting section
2. Review application logs in `logs/app.log`
3. Check that you're running the latest version

---

**Made with ❤️ for keeping your PC clean and secure!**
