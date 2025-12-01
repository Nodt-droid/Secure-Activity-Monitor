███████╗███████╗ ██████╗██╗   ██╗██████╗ ███████╗
██╔════╝██╔════╝██╔════╝██║   ██║██╔══██╗██╔════╝
███████╗█████╗  ██║     ██║   ██║██████╔╝█████╗  
╚════██║██╔══╝  ██║     ██║   ██║██╔══██╗██╔══╝  
███████║███████╗╚██████╗╚██████╔╝██║  ██║███████╗
╚══════╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝

    Secure Activity Monitor — Python Edition  
       Ethical • Encrypted • Transparent
       ![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey)
![License](https://img.shields.io/badge/License-MIT-green)
![Security](https://img.shields.io/badge/Encrypted-AES256-purple)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)
## 🔍 About This Project
Secure Activity Monitor is a privacy-focused tool designed for **ethical testing, debugging, and workflow analytics**.

This project demonstrates:
- Secure software design  
- Encrypted data logging  
- Real-time event tracking  
- Ethical monitoring principles  
- Windows API integration (active window tracking)  
- Modular Python architecture  

It is **not** a keylogger, spyware, or stealth surveillance tool.
All monitoring is transparent, visible, and safe.

                   ┌────────────────────┐
                   │    User Actions     │
                   │ (Keyboard / Mouse)  │
                   └─────────┬──────────┘
                             │
                             ▼
                 ┌────────────────────────┐
                 │  Event Processing Core │
                 │  - Detect key events   │
                 │  - Mouse clicks/scroll │
                 │  - Copy/Paste signals  │
                 └─────────┬─────────────┘
                           │
                           ▼
              ┌──────────────────────────────┐
              │   Context Collector          │
              │ - Timestamp                  │
              │ - Active window title        │
              └───────────┬─────────────────┘
                          │
                          ▼
                 ┌────────────────────┐
                 │ AES-256 Encryption │
                 │ (EAX Mode)        │
                 └─────────┬──────────┘
                           │
                           ▼
              ┌──────────────────────────────┐
              │   Encrypted Log Writer       │
              │ - Unified log file           │
              │ - Auto-log rotation          │
              └──────────────────────────────┘

## 🖥️ Live Preview (Terminal Output Example)

[2025-01-20 18:22:41] [KEY] a | Window: Visual Studio Code
[2025-01-20 18:22:42] [KEY] Key.space | Window: Visual Studio Code
[2025-01-20 18:22:43] [COPY] User pressed CTRL+C | Window: Chrome
[2025-01-20 18:22:45] [MOUSE CLICK] Button.left at (822,511)
[2025-01-20 18:22:47] [SCROLL] (0,-1) at (901,320)

## 📦 Installation

```bash
git clone https://github.com/your-username/Secure-Activity-Monitor
cd Secure-Activity-Monitor
pip install -r requirements.txt
python monitor.py
