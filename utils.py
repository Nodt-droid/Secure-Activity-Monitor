import os
import time
import win32gui
import psutil

LOG_FILE = "logs/activity.log"
MAX_SIZE = 1_000_000  # 1MB rotate threshold


def get_active_window():
    try:
        hwnd = win32gui.GetForegroundWindow()
        title = win32gui.GetWindowText(hwnd)
        return title if title else "Unknown Window"
    except:
        return "Unknown Window"


def rotate_logs():
    if os.path.exists(LOG_FILE) and os.path.getsize(LOG_FILE) > MAX_SIZE:
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        os.rename(LOG_FILE, f"logs/activity_{timestamp}.log")


def timestamp():
    return time.strftime("[%Y-%m-%d %H:%M:%S]")
