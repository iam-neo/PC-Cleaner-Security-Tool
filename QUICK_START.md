# 🚀 Quick Start Guide - PC Cleaner & Security Tool

## ⚡ 5-Minute Setup

### Step 1: Install Dependencies (30 seconds)
```bash
cd c:\xampp\htdocs\pro
pip install -r requirements.txt
```

### Step 2: Run the Application (10 seconds)
```bash
python pc_cleaner_app.py
```

**Or run as Administrator** (Recommended):
```powershell
Start-Process python -ArgumentList "pc_cleaner_app.py" -Verb RunAs
```

### Step 3: Start Cleaning! (2 minutes)

#### Option A: Quick Clean
1. Click **"🧹 PC Cleaner"** in the sidebar
2. Click **"Start Scan"**
3. Wait for scan to complete
4. Click **"Clean Selected"**
5. Type **"YES"** and confirm
6. Done! 🎉

#### Option B: Quick Malware Scan
1. Click **"🛡️ Malware Scanner"** in the sidebar
2. Click **"Quick Scan"**
3. Wait for scan to complete
4. Review any threats found
5. Click **"Quarantine"** or **"Delete"** for each threat
6. Done! 🎉

---

## 📋 What This Tool Does

### ✅ PC Cleaner
- Removes temporary files
- Clears browser cache
- Empties Recycle Bin
- **Result**: Free up disk space (typically 1-10 GB)

### ✅ Malware Scanner
- Scans for suspicious files
- Checks running processes
- Detects known malware patterns
- **Result**: Identify and remove threats

---

## 🎯 First Time Checklist

- [ ] Install Python 3.8+ (if not already installed)
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Run as Administrator for full functionality
- [ ] Perform initial PC clean to free up space
- [ ] Run Quick Scan to check for malware
- [ ] Review the full [USER_GUIDE.md](USER_GUIDE.md) for detailed instructions

---

## ⚠️ Important Notes

### Administrator Privileges
**Why you need it:**
- Access all system directories
- Delete protected files
- Terminate suspicious processes
- Empty Recycle Bin completely

**How to run as admin:**
- Right-click → "Run as administrator"
- Or use PowerShell command above

### Safety First
- ✅ All files are reviewed before deletion
- ✅ Confirmation required for destructive actions
- ✅ Quarantine system for suspicious files
- ✅ Protected system paths are never touched

---

## 🔧 Building Standalone .exe

Want to run without Python? Build an executable:

```bash
python build.py
```

The `.exe` file will be in `dist/PCCleanerTool.exe`

**Benefits:**
- No Python required
- Faster startup
- Easier to share
- Professional appearance

---

## 📚 Need More Help?

- **Full Documentation**: See [USER_GUIDE.md](USER_GUIDE.md)
- **Features**: See [README.md](README.md)
- **Configuration**: Edit `config.py`
- **Logs**: Check `logs/app.log` for errors

---

## 🎨 Customization

### Change Theme
1. Click **"Appearance Mode"** at the bottom of sidebar
2. Choose: Light, Dark, or System

### Adjust Settings
Edit `config.py`:
- Change scan paths
- Modify file extensions
- Adjust UI settings
- Configure malware signatures

---

## 📊 Typical Results

### After First Clean:
- **Temp Files**: 500 MB - 5 GB freed
- **Browser Cache**: 200 MB - 2 GB freed
- **Recycle Bin**: 100 MB - 10 GB freed
- **Total**: 1 GB - 15 GB freed on average

### After First Scan:
- **Quick Scan**: 0-5 threats (typically false positives)
- **Full Scan**: 0-10 threats (varies by PC usage)
- **Process Scan**: 0-2 suspicious processes

---

## 🔄 Recommended Schedule

### Daily (1 minute)
- Quick Clean from Dashboard

### Weekly (5 minutes)
- Full PC Clean
- Quick Malware Scan

### Monthly (30 minutes)
- Full Malware Scan
- Review quarantined files
- Update malware signatures

---

## ✨ Pro Tips

1. **Close browsers** before cleaning cache
2. **Save your work** before cleaning
3. **Use Quarantine** instead of Delete for uncertain threats
4. **Review logs** in `logs/app.log` after cleaning
5. **Keep Windows Defender** enabled alongside this tool

---

## 🆘 Quick Troubleshooting

### Can't delete files?
→ Run as Administrator

### Scan too slow?
→ Use Quick Scan instead of Full Scan

### False positives?
→ Use Quarantine, then verify with Windows Defender

### App won't start?
→ Check Python version: `python --version` (need 3.8+)

---

**Ready to clean your PC? Let's go! 🚀**

For detailed instructions, see [USER_GUIDE.md](USER_GUIDE.md)
