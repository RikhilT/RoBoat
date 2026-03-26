import threading
import time
stop_event = threading.Event()

def start():
    print("Starting Challenge 3")

    while not stop_event.is_set():
        print("Doing Challenge 3")
        time.sleep(0.5)
        pass

def stop():
    print("Stopping Challenge 3")
    stop_event.set()