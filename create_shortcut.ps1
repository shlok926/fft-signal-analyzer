$DesktopPath = [Environment]::GetFolderPath("Desktop")
$ShortcutPath = Join-Path $DesktopPath "FFT Spectrum Analyzer.lnk"
$AppBatPath = "c:\Users\Shlok\fft_signal_analyzer\FFT_Spectrum_Analyzer.bat"
$AppDir = "c:\Users\Shlok\fft_signal_analyzer"

# Create WScript shell object
$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut($ShortcutPath)

# Set shortcut properties
$Shortcut.TargetPath = $AppBatPath
$Shortcut.WorkingDirectory = $AppDir
$Shortcut.WindowStyle = 1  # Normal window
$Shortcut.IconLocation = "C:\Users\Shlok\fft_signal_analyzer\src\fft_analyzer\assets\icon.ico"  # Optional custom icon
$Shortcut.Description = "Launch FFT Spectrum Analyzer"

# Save the shortcut
$Shortcut.Save()

Write-Host "✅ Desktop shortcut created: $ShortcutPath"
Write-Host "📍 Target: $AppBatPath"
Write-Host "📂 Working Directory: $AppDir"
