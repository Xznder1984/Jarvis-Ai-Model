$Root = Split-Path -Parent $PSScriptRoot
& "$Root\.venv\Scripts\pip.exe" install pyinstaller
& "$Root\.venv\Scripts\pyinstaller.exe" --noconfirm --onefile --name Jarvis "$Root\jarvis_app\main.py"
Write-Host "EXE created in dist\Jarvis.exe"
