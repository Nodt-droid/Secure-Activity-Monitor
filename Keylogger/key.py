# input_monitor.py
import threading
import sys
import os
from datetime import datetime
import platform

from pynput.keyboard import Listener as KeyboardListener, Key
from pynput.mouse import Listener as MouseListener

# ---------- CONFIG---------
LOG_FILE = "monitor_log.txt"
PRINT_TO_CONSOLE = True
# ----------------------------

def get_active_window_title():
    try:
        system = platform.system()
        if system == "Windows":
            import ctypes
            user32 = ctypes.windll.user32
            kernel32 = ctypes.windll.kernel32
            hwnd = user32.GetForegroundWindow()
            if hwnd == 0:
                return "<No active window>"
            length = user32.GetWindowTextLengthW(hwnd)
            buff = ctypes.create_unicode_buffer(length + 1)
            user32.GetWindowTextW(hwnd, buff, length + 1)
            return buff.value
        elif system == "Darwin":
            try:
                from AppKit import NSWorkspace
                active_app = NSWorkspace.sharedWorkspace().frontmostApplication()
                return active_app.localizedName() or "<Unknown App>"
            except Exception:
                return "<Active window title unavailable on macOS (pyobjc optional)>"
        else:
            try:
                import subprocess
                root = subprocess.check_output(["xprop", "-root", "_NET_ACTIVE_WINDOW"], stderr=subprocess.DEVNULL).decode()
                # parse window id
                if "WINDOW" in root:
                    wid = root.strip().split()[-1]
                    out = subprocess.check_output(["xprop", "-id", wid, "WM_NAME"], stderr=subprocess.DEVNULL).decode()
                    # WM_NAME(STRING) = "title"
                    if "=" in out:
                        return out.split("=", 1)[1].strip().strip('"')
                return "<Active window title unavailable>"
            except Exception:
                return "<Active window title unavailable>"
    except Exception:
        return "<Error retrieving window title>"

def timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def log_event(line):
    entry = f"[{timestamp()}] {line}\n"
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(entry)
    if PRINT_TO_CONSOLE:
        print(entry, end="")

# ---------------- Keyboard handling ----------------
pressed_modifiers = set()  # track Ctrl/Alt/Shift/Cmd state

def on_press(key):
    try:
        kname = key.char 
    except AttributeError:
        kname = str(key)  

    name = kname if isinstance(kname, str) else str(kname)

    if name in ("Key.ctrl_l", "Key.ctrl_r", "Key.ctrl"):
        pressed_modifiers.add("ctrl")
    if name in ("Key.cmd", "Key.cmd_l", "Key.cmd_r"):
        pressed_modifiers.add("cmd")
    if name in ("Key.shift", "Key.shift_l", "Key.shift_r"):
        pressed_modifiers.add("shift")
    if name in ("Key.alt", "Key.alt_l", "Key.alt_r"):
        pressed_modifiers.add("alt")

    is_ctrl = ("ctrl" in pressed_modifiers) or ("cmd" in pressed_modifiers)
    simple_key = ''
    if hasattr(key, "char") and key.char is not None:
        simple_key = key.char.lower()
    elif isinstance(key, Key):
        simple_key = str(key)

    if is_ctrl and simple_key == "c":
        win = get_active_window_title()
        log_event(f"[COPY EVENT] Window: {win}  (Ctrl/Cmd+C pressed)")
        return  
    if is_ctrl and simple_key == "v":
        win = get_active_window_title()
        log_event(f"[PASTE EVENT] Window: {win}  (Ctrl/Cmd+V pressed)")
        return

    if isinstance(key, Key):
        keyname = str(key).replace("Key.", "").capitalize()
    else:
        keyname = str(key).replace("'", "")

    win = get_active_window_title()
    log_event(f"[KEY] Window: {win}  Key: {keyname}")

def on_release(key):
    try:
        name = key.char
    except Exception:
        name = str(key)
    if name in ("Key.ctrl_l", "Key.ctrl_r", "Key.ctrl"):
        pressed_modifiers.discard("ctrl")
    if name in ("Key.cmd", "Key.cmd_l", "Key.cmd_r"):
        pressed_modifiers.discard("cmd")
    if name in ("Key.shift", "Key.shift_l", "Key.shift_r"):
        pressed_modifiers.discard("shift")
    if name in ("Key.alt", "Key.alt_l", "Key.alt_r"):
        pressed_modifiers.discard("alt")

# ---------------- Mouse handling ----------------
def on_click(x, y, button, pressed):
    action = "Pressed" if pressed else "Released"
    win = get_active_window_title()
    log_event(f"[MOUSE] Window: {win}  {action} {button} at ({x}, {y})")

def on_scroll(x, y, dx, dy):
    win = get_active_window_title()
    log_event(f"[MOUSE SCROLL] Window: {win}  at ({x}, {y})  delta=({dx},{dy})")

# ---------------- Thread listeners ----------------
def keyboard_thread_fn():
    with KeyboardListener(on_press=on_press, on_release=on_release) as kl:
        kl.join()

def mouse_thread_fn():
    with MouseListener(on_click=on_click, on_move=on_move, on_scroll=on_scroll) as ml:
        ml.join()

def ensure_log_file_header():
    if not os.path.exists(LOG_FILE) or os.path.getsize(LOG_FILE) == 0:
        header = (
            "=== Input Monitor Log ===\n"
            f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"Platform: {platform.platform()}\n"
            "NOTE: This monitor logs key names and events. It does NOT capture clipboard contents or hidden data.\n\n"
        )
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(header)
        if PRINT_TO_CONSOLE:
            print(header, end="")

def main():
    print("INPUT MONITOR — Visible mode\nThis tool logs key names, mouse clicks, timestamps and active window titles.")
    print("Logs are written to:", os.path.abspath(LOG_FILE))
    print("Press Ctrl+C in this terminal to stop.\n")
    ensure_log_file_header()

    kt = threading.Thread(target=keyboard_thread_fn, daemon=True)
    mt = threading.Thread(target=mouse_thread_fn, daemon=True)

    kt.start()
    mt.start()

    try:
        while True:
            kt.join(timeout=1)
            mt.join(timeout=1)
            if not kt.is_alive() and not mt.is_alive():
                break
    except KeyboardInterrupt:
        print("\nStopping monitor... (Ctrl+C received)")

if __name__ == "__main__":
    main()
