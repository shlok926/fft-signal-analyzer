$DesktopPath = [Environment]::GetFolderPath("Desktop")
$ShortcutPath = Join-Path $DesktopPath "FFT Spectrum Analyzer.lnk"
$AppBatPath = Join-Path $PSScriptRoot "FFT_Spectrum_Analyzer.bat"
$AppDir = $PSScriptRoot

# Create WScript shell object
$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut($ShortcutPath)

# Set shortcut properties
$Shortcut.TargetPath = $AppBatPath
$Shortcut.WorkingDirectory = $AppDir
$Shortcut.WindowStyle = 1  # Normal window
$Shortcut.Description = "Launch FFT Spectrum Analyzer"

# Save the shortcut
$Shortcut.Save()

Write-Host "✅ Desktop shortcut created: $ShortcutPath"
Write-Host "📍 Target: $AppBatPath"
Write-Host "📂 Working Directory: $AppDir"
