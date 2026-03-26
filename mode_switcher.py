import networking
import threading
import time
import pickle
from xbox import xbox_controller_functions as xcf

current_mode = None
new_mode = None

def change_mode(mode_num):
    global new_mode
    new_mode = mode_num

stop_event = threading.Event()
def stop_manual_control_thread():
    stop_event.set()

def manual_control_thread():
    global current_mode, new_mode
    last_controller_send = 0.0
    controller_interval = 0.1
    # Use wait to yield CPU and be responsive to stop_event
    while not stop_event.wait(0.01):
        try:
            mode = new_mode
            if mode is not None and mode != current_mode:
                try:
                    networking.add_to_send_buffer(mode.to_bytes(4, byteorder='big'), 4)
                    current_mode = mode
                except Exception:
                    print("Error sending mode switch notification")
                    # avoid crashing if send buffer fails; continue loop
                    pass

            if current_mode == 11:  # Manual control mode
                now = time.time()
                if now - last_controller_send >= controller_interval:
                    try:
                        controller_data = xcf.get_controller_values()
                        data = pickle.dumps(controller_data)
                        networking.add_to_send_buffer(data, 3)
                        last_controller_send = now
                    except Exception:
                        print("Error sending controller data")
                        # swallow send/serialization errors to avoid blocking the loop
                        pass
        except Exception:
            # protect thread from unexpected errors
            print("Error in manual control thread:")
            pass

    print("Manual control thread stopping")