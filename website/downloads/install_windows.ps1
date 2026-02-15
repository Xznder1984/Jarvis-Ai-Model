$Root = Split-Path -Parent $PSScriptRoot
py -m venv "$Root\.venv"
& "$Root\.venv\Scripts\pip.exe" install --upgrade pip
& "$Root\.venv\Scripts\pip.exe" install -r "$Root\requirements.txt"

$launcher = "@echo off`r`n`"$Root\.venv\Scripts\python.exe`" -m jarvis_app.main %*"
Set-Content -Path "$Root\Jarvis.bat" -Value $launcher

Write-Host "Installed. Run Jarvis.bat or build an .exe with PyInstaller."
