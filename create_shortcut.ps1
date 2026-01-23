# PC Cleaner & Security Tool - Desktop Shortcut Creator
# This script creates a desktop shortcut for easy access

$WScriptShell = New-Object -ComObject WScript.Shell
$Desktop = [System.Environment]::GetFolderPath('Desktop')
$ShortcutPath = Join-Path $Desktop "PC Cleaner Tool.lnk"
$TargetPath = "python.exe"
$Arguments = "c:\xampp\htdocs\pro\pc_cleaner_app.py"
$WorkingDirectory = "c:\xampp\htdocs\pro"
$IconLocation = "c:\xampp\htdocs\pro\resources\icon.png"

$Shortcut = $WScriptShell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = $TargetPath
$Shortcut.Arguments = $Arguments
$Shortcut.WorkingDirectory = $WorkingDirectory
$Shortcut.IconLocation = $IconLocation
$Shortcut.Description = "PC Cleaner & Security Tool - Clean temp files and scan for malware"
$Shortcut.WindowStyle = 1  # Normal window

try {
    $Shortcut.Save()
    Write-Host "✅ Desktop shortcut created successfully!" -ForegroundColor Green
    Write-Host "📍 Location: $ShortcutPath" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "To run as Administrator:" -ForegroundColor Yellow
    Write-Host "  Right-click the shortcut → Properties → Advanced → Run as administrator" -ForegroundColor Yellow
} catch {
    Write-Host "❌ Error creating shortcut: $_" -ForegroundColor Red
}
