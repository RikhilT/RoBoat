import modes
import threading
import importlib


mode_map = {
        1: __import__('modes.challenge1', fromlist=['start', 'stop']),
        2: __import__('modes.challenge2', fromlist=['start', 'stop']),
        3: __import__('modes.challenge3', fromlist=['start', 'stop']),
        4: __import__('modes.challenge4', fromlist=['start', 'stop']),
        5: __import__('modes.challenge5', fromlist=['start', 'stop']),
        6: __import__('modes.challenge6', fromlist=['start', 'stop']),
        7: __import__('modes.challenge7', fromlist=['start', 'stop']),
        8: __import__('modes.challenge8', fromlist=['start', 'stop']),
        9: __import__('modes.challenge9', fromlist=['start', 'stop']),
        10: __import__('modes.challenge10', fromlist=['start', 'stop']),
        11: __import__('modes.manual_control', fromlist=['start', 'stop']),
        12: __import__('modes.mode_stop', fromlist=['start', 'stop']),
}

current_module = mode_map.get(12)
current_thread = None
current_mode = 12

def switch_mode(new_mode):
    global current_thread, current_module, current_mode, mode_map

    target_module = mode_map.get(new_mode) or mode_map.get(12)

    # If the requested mode is already running, nothing to do.
    if new_mode == current_mode and current_thread and current_thread.is_alive():
        return

    # Stop currently running mode if any
    if current_thread and current_thread.is_alive():
        try:
            current_module.stop()
        except Exception:
            pass
        current_thread.join(timeout=2)

    # Reload the target module to reset module-level state so it can be started again
    try:
        target_module = importlib.reload(target_module)
    except Exception:
        target_module = mode_map.get(12)

    # Start the new mode in a fresh thread
    current_module = target_module
    if new_mode == 12:
        print("Switched to STOP mode")
    else:
        current_thread = threading.Thread(target=current_module.start, daemon=True)
        current_thread.start()
        print(f"Switched to mode {new_mode}")
    current_mode = new_mode
