# Jarvis AI Model (Secure Desktop Assistant)

A cross-platform "Jarvis-style" assistant with:
- GUI app for chat + device controls
- Encrypted API key vault saved in binary-style file (`~/.jarvis/secrets.bin`)
- Provider flexibility: use your own API key (OpenAI-compatible endpoint) or local fallback AI mode
- Camera/projector detection with explicit user permission toggles
- Linux command launcher (`Jarvis`) and Windows executable workflow
- Minimalistic download/info website included in `website/`

> Note: This project is inspired by futuristic assistants, but it is **not** a literal/identical Tony Stark cinematic AI.

## System targets
- RAM: at least **4 GB**
- Disk: around **0.25 GB** free recommended
- OS: Linux and Windows

## Quick start

### Linux (method 1: curl)
```bash
curl -fsSL https://raw.githubusercontent.com/Xznder1984/Jarvis-Ai-Model/main/website/downloads/install_linux.sh | bash
```

### Linux (method 2: git)
```bash
git clone https://github.com/Xznder1984/Jarvis-Ai-Model.git
cd Jarvis-Ai-Model
bash scripts/install_linux.sh
Jarvis
```

### Windows (method 1: installer)
- Download `JarvisSetup.exe` (generated in your release pipeline).
- Run installer, then launch desktop shortcut or `Jarvis.exe`.

### Windows (method 2: git)
```powershell
git clone https://github.com/Xznder1984/Jarvis-Ai-Model.git
cd Jarvis-Ai-Model
powershell -ExecutionPolicy Bypass -File scripts/install_windows.ps1
.\Jarvis.bat
```

To build native exe:
```powershell
powershell -ExecutionPolicy Bypass -File scripts/build_windows_exe.ps1
```
Produces: `dist\Jarvis.exe`

## Features
- **Security vault**
  - API keys are encrypted at rest (PBKDF2-derived stream key + binary vault file).
  - Each record includes a random digest hash for tamper-evident metadata.
- **AI engine**
  - `local` mode for built-in assistant responses.
  - `openai-compatible` mode for user API keys + endpoint/model selection.
- **Device controls**
  - Camera availability scan.
  - External-display/projector detection.
  - Permission toggles for camera/projector usage.

## App usage
1. Open **Security & AI** tab.
2. Select provider (`local` or `openai-compatible`).
3. Add API key and click **Save Key Securely**.
4. In **Devices**, click **Detect Devices** and grant permissions.
5. In **Assistant**, ask Jarvis questions.

## Website
Open locally:
- `website/index.html`

Hosted downloads in this repo:
- `website/downloads/install_linux.sh`
- `website/downloads/install_windows.ps1`

Includes:
- Download sections for Linux + Windows
- Project information
- Credits tab section

## Credits
- Developer: GPT-5.2-Codex (OpenAI)
- Designer: You

