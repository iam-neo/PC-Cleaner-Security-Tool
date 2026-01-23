# 🛡️ PC Cleaner & Security Tool - Complete User Guide

## Table of Contents
1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [Features Overview](#features-overview)
4. [Using the Dashboard](#using-the-dashboard)
5. [PC Cleaner Guide](#pc-cleaner-guide)
6. [Malware Scanner Guide](#malware-scanner-guide)
7. [Safety & Best Practices](#safety--best-practices)
8. [Troubleshooting](#troubleshooting)
9. [FAQ](#faq)

---

## Introduction

Welcome to **PC Cleaner & Security Tool**! This application helps you:
- ✅ Remove unnecessary temporary files and cache
- ✅ Free up disk space on your PC
- ✅ Scan for malware and suspicious files
- ✅ Monitor system health and performance

### System Requirements
- **Operating System**: Windows 10 or later
- **Python**: 3.8 or higher (if running from source)
- **Permissions**: Administrator privileges recommended

---

## Getting Started

### First Time Setup

1. **Install Dependencies** (if running from source):
   ```bash
   pip install -r requirements.txt
   ```

2. **Launch the Application**:
   ```bash
   python pc_cleaner_app.py
   ```

3. **Run as Administrator** (Recommended):
   - Right-click on `pc_cleaner_app.py`
   - Select "Run as administrator"
   
   Or use PowerShell:
   ```powershell
   Start-Process python -ArgumentList "pc_cleaner_app.py" -Verb RunAs
   ```

### Understanding Administrator Privileges

⚠️ **Why Administrator Access is Important:**

Without administrator privileges, the application has limited functionality:
- ❌ Cannot access all system temp directories
- ❌ Cannot delete protected files
- ❌ Cannot terminate system processes
- ❌ Cannot empty Recycle Bin completely

The application will show a warning if not running as administrator.

---

## Features Overview

### 🧹 PC Cleaner
Removes unnecessary files to free up disk space:
- Temporary files from system temp directories
- Browser cache (Chrome, Edge, Firefox, Opera)
- Windows Recycle Bin
- Old log files and backup files

### 🛡️ Malware Scanner
Scans your PC for potential threats:
- **Quick Scan**: Scans common malware locations (fast)
- **Full Scan**: Comprehensive system-wide scan (thorough)
- **Process Scanner**: Checks running processes for suspicious activity
- **Quarantine System**: Safely isolate threats before deletion

### 📊 Dashboard
Monitor your system at a glance:
- System information (OS, processor, memory)
- Disk usage statistics
- Quick access to cleaning and scanning
- Recent scan history

---

## Using the Dashboard

### Overview
The Dashboard is your command center, showing:
- **System Info**: OS version, processor, Python version
- **Disk Usage**: Total, used, and free space on C: drive
- **Quick Actions**: Fast access to cleaning and scanning

### Quick Actions

1. **Quick Clean**
   - Click to jump directly to PC Cleaner tab
   - Starts a scan immediately

2. **Quick Scan**
   - Click to jump directly to Malware Scanner tab
   - Ready to start malware scanning

3. **Refresh Dashboard**
   - Updates all statistics
   - Refreshes disk usage information

---

## PC Cleaner Guide

### Step-by-Step Cleaning Process

#### Step 1: Start a Scan
1. Navigate to the **🧹 PC Cleaner** tab
2. Click the **"Start Scan"** button
3. Wait while the application scans your system

**What's Being Scanned:**
- `%TEMP%` - User temporary files
- `%TMP%` - System temporary files
- `C:\Windows\Temp` - Windows temp directory
- Browser cache directories
- Recycle Bin

#### Step 2: Review Scan Results
After scanning, you'll see:
- **Total Items Found**: Number of files/folders
- **Total Size**: Space that can be freed
- **Category Breakdown**:
  - Temporary Files
  - Browser Cache (per browser)
  - Recycle Bin

#### Step 3: Select Files to Clean
- ✅ All files are selected by default
- ⬜ Uncheck any files you want to keep
- 📁 Click on categories to expand/collapse

**Categories Explained:**
- **Temporary Files**: Safe to delete, created by applications
- **Browser Cache**: Speeds up browsing but can be recreated
- **Recycle Bin**: Already deleted files, safe to remove permanently

#### Step 4: Clean Selected Files
1. Click **"Clean Selected"** button
2. A confirmation dialog appears
3. Type **"YES"** (in capital letters) to confirm
4. Click **"Confirm"** to proceed

⚠️ **Warning**: This action cannot be undone!

#### Step 5: View Results
After cleaning:
- **Files Deleted**: Number of successfully removed items
- **Space Freed**: Amount of disk space recovered
- **Errors**: Any files that couldn't be deleted (if any)

### Special Features

#### Empty Recycle Bin
- Separate button to empty Recycle Bin only
- Permanently deletes all files in Recycle Bin
- Requires confirmation

#### Refresh Scan
- Re-scan without closing the tab
- Useful after cleaning to verify results

---

## Malware Scanner Guide

### Understanding Malware Detection

This tool uses multiple detection methods:

1. **Pattern Matching**: Identifies suspicious file patterns
   - Double extensions (e.g., `.exe.exe`)
   - Screensaver files (`.scr`)
   - Program Information Files (`.pif`)

2. **Hash-Based Detection**: Compares file hashes against known malware
   - MD5 hash comparison
   - Signature database in `resources/malware_signatures.json`

3. **Location-Based Detection**: Finds system files in wrong locations
   - `svchost.exe` outside System32
   - `csrss.exe` outside System32
   - `winlogon.exe` outside System32

4. **Behavioral Analysis**: Detects suspicious behaviors
   - Hidden executable files
   - Suspicious process activity

### Scan Types

#### Quick Scan (Recommended for Regular Use)
**What it scans:**
- `%TEMP%` directory
- `%APPDATA%` directory
- Downloads folder

**Duration**: 1-5 minutes

**Best for:**
- Daily/weekly security checks
- Quick verification after downloads
- Routine maintenance

#### Full Scan (Thorough Protection)
**What it scans:**
- Entire C: drive
- All executable files
- All script files

**Duration**: 15-60 minutes (depending on drive size)

**Best for:**
- Monthly deep scans
- After suspicious activity
- New PC setup

#### Process Scan
**What it checks:**
- All running processes
- Process locations
- Suspicious process names

**Duration**: Less than 1 minute

**Best for:**
- Real-time threat detection
- Checking active malware
- Performance issues

### Step-by-Step Scanning

#### Step 1: Choose Scan Type
1. Navigate to **🛡️ Malware Scanner** tab
2. Select scan type:
   - Click **"Quick Scan"** for fast scan
   - Click **"Full Scan"** for thorough scan
   - Click **"Scan Processes"** for active threats

#### Step 2: Monitor Scan Progress
- Progress bar shows completion percentage
- Current file being scanned is displayed
- Scan can take several minutes

⚠️ **Note**: Do not close the application during scanning!

#### Step 3: Review Detected Threats
For each threat, you'll see:
- **File Name**: Name of the suspicious file
- **Path**: Full location on your PC
- **Size**: File size
- **Threat Type**: What made it suspicious
- **Severity**: Low, Medium, High, or Critical

**Severity Levels:**
- 🟢 **Low**: Minor suspicion, likely false positive
- 🟡 **Medium**: Suspicious pattern detected
- 🟠 **High**: Strong indicators of malware
- 🔴 **Critical**: Known malware signature

#### Step 4: Handle Threats
For each detected threat, you have three options:

1. **Quarantine** (Recommended)
   - Moves file to quarantine folder
   - File is isolated but not deleted
   - Can be restored if false positive
   - Location: `quarantine/` folder

2. **Delete**
   - Permanently removes the file
   - Cannot be recovered
   - Use for confirmed threats only

3. **Ignore**
   - Keeps the file
   - Use for known safe files
   - File remains in original location

#### Step 5: Process Scanner Results
If scanning processes:
- **Suspicious Process**: Process name and PID
- **Location**: Where the process is running from
- **Reason**: Why it's flagged as suspicious

**Actions:**
- **Terminate**: Stops the process immediately
- **Ignore**: Allows process to continue

⚠️ **Warning**: Terminating system processes can cause system instability!

### Understanding False Positives

**What is a False Positive?**
A false positive occurs when a safe file is incorrectly identified as malware.

**Common False Positives:**
- Development tools and compilers
- Custom scripts and automation tools
- Legitimate software with unusual patterns
- System files in non-standard locations (portable apps)

**How to Handle:**
1. Check the file location and name
2. Verify the file is from a trusted source
3. Use **Quarantine** instead of **Delete**
4. Scan with Windows Defender for second opinion
5. If confirmed safe, click **Ignore**

---

## Safety & Best Practices

### Before Cleaning

✅ **Do:**
- Close all browsers before cleaning browser cache
- Save your work in all applications
- Run as administrator for full functionality
- Review scan results carefully

❌ **Don't:**
- Delete files you're unsure about
- Clean while important applications are running
- Ignore protected path warnings

### Before Scanning

✅ **Do:**
- Close unnecessary applications
- Ensure you have time for full scan to complete
- Back up important data regularly
- Keep Windows Defender enabled

❌ **Don't:**
- Interrupt scans in progress
- Delete files without reviewing threat details
- Rely solely on this tool for security

### Protected Paths

These directories are **NEVER** scanned or cleaned:
- `C:\Windows\System32`
- `C:\Windows\SysWOW64`
- `C:\Program Files`
- `C:\Program Files (x86)`
- `C:\Windows\WinSxS`

### Data Safety

**Quarantine System:**
- Quarantined files are stored in `quarantine/` folder
- Files are moved, not deleted
- Can be manually restored if needed
- Quarantine folder can be cleared manually

**Logging:**
- All actions are logged in `logs/app.log`
- Review logs to see what was deleted
- Useful for troubleshooting

---

## Troubleshooting

### Common Issues

#### "Permission Denied" Errors

**Problem**: Cannot delete certain files

**Solutions:**
1. Run application as administrator
2. Close applications using those files
3. Restart PC and try again
4. Check file is not read-only

#### Scan Takes Too Long

**Problem**: Full scan running for hours

**Solutions:**
1. Use Quick Scan instead
2. Adjust `MAX_FILE_SIZE_MB` in `config.py`
3. Close other applications
4. Check disk for errors

#### Application Won't Start

**Problem**: Application crashes on launch

**Solutions:**
1. Check Python version (3.8+)
2. Reinstall dependencies:
   ```bash
   pip install -r requirements.txt --upgrade
   ```
3. Check `logs/app.log` for errors
4. Verify all files are present

#### False Positives in Scanner

**Problem**: Safe files detected as malware

**Solutions:**
1. Review threat details carefully
2. Use Quarantine instead of Delete
3. Check file with Windows Defender
4. Update signatures in `resources/malware_signatures.json`

#### Cannot Empty Recycle Bin

**Problem**: Recycle Bin won't empty

**Solutions:**
1. Run as administrator
2. Close File Explorer
3. Restart PC
4. Use Windows built-in tool as backup

---

## FAQ

### General Questions

**Q: Is this a replacement for antivirus software?**
A: No. This tool provides basic malware detection but should be used alongside professional antivirus software like Windows Defender.

**Q: Is it safe to delete all temporary files?**
A: Yes, temporary files are safe to delete. Applications will recreate them as needed.

**Q: Will cleaning browser cache log me out of websites?**
A: No, cache is different from cookies. You'll stay logged in, but websites may load slightly slower on first visit.

**Q: How often should I clean my PC?**
A: Weekly cleaning is recommended for regular users. Daily for heavy users.

**Q: How often should I scan for malware?**
A: Quick scan weekly, full scan monthly, or after suspicious activity.

### Technical Questions

**Q: Where are quarantined files stored?**
A: In the `quarantine/` folder in the application directory.

**Q: Can I customize what gets scanned?**
A: Yes, edit `config.py` to customize scan paths and file extensions.

**Q: Does this work on Windows 11?**
A: Yes, fully compatible with Windows 10 and Windows 11.

**Q: Can I run this on a schedule?**
A: Not built-in, but you can use Windows Task Scheduler to run the application.

**Q: How do I update malware signatures?**
A: Edit `resources/malware_signatures.json` and add new hashes/patterns.

### Privacy Questions

**Q: Does this send data to the internet?**
A: No, all scanning and cleaning is done locally. No data is sent anywhere.

**Q: Can I use this offline?**
A: Yes, fully functional without internet connection.

**Q: Is my data safe?**
A: Yes, the application only deletes files you approve. All actions are logged.

---

## Advanced Configuration

### Editing config.py

You can customize the application by editing `config.py`:

```python
# Change UI theme
THEME_MODE = "dark"  # or "light"

# Adjust scan settings
MAX_FILE_SIZE_MB = 100  # Maximum file size to scan

# Add custom temp directories
TEMP_DIRECTORIES = [
    os.environ.get('TEMP'),
    r'C:\CustomTemp',  # Add your custom path
]

# Add custom file extensions
TEMP_FILE_EXTENSIONS = [
    '.tmp', '.temp', '.bak',
    '.custom',  # Add your extension
]
```

### Updating Malware Signatures

Edit `resources/malware_signatures.json`:

```json
{
  "hashes": {
    "d41d8cd98f00b204e9800998ecf8427e": "Generic.Trojan",
    "your_malware_hash_here": "Malware.Name"
  },
  "patterns": [
    ".*\\.exe\\.exe$",
    "your_custom_pattern"
  ],
  "suspicious_names": [
    "svchost.exe",
    "your_suspicious_filename.exe"
  ]
}
```

---

## Building Standalone Executable

To create a `.exe` file that runs without Python:

```bash
python build.py
```

The executable will be in `dist/PCCleanerTool.exe`

**Benefits:**
- No Python installation required
- Easier to distribute
- Faster startup time
- Professional appearance

---

## Support & Feedback

### Getting Help

1. Check this user guide
2. Review `logs/app.log` for errors
3. Check the Troubleshooting section
4. Verify you're running the latest version

### Reporting Issues

When reporting issues, include:
- Windows version
- Python version (if running from source)
- Error message from logs
- Steps to reproduce the issue

---

## Changelog

### Version 1.0.0
- ✅ PC Cleaner with temp file removal
- ✅ Browser cache cleaning
- ✅ Malware scanner with multiple detection methods
- ✅ Dashboard with system monitoring
- ✅ Quarantine system
- ✅ Dark/Light theme support
- ✅ Administrator privilege detection

---

## Credits

**PC Cleaner & Security Tool** v1.0.0

Made with ❤️ for keeping your PC clean and secure!

### Technologies Used
- **CustomTkinter**: Modern UI framework
- **psutil**: System and process utilities
- **Pillow**: Image processing
- **PyInstaller**: Executable builder

---

**⚠️ Disclaimer**: This tool is provided as-is for educational and personal use. Always maintain regular backups of important data. For comprehensive security, use professional antivirus software alongside this tool.
