import threading
import time
stop_event = threading.Event()

def start():
    print("Starting Challenge 1")

    while not stop_event.is_set():
        print("Doing Challenge 1")
        time.sleep(0.5)
        pass

def stop():
    print("Stopping Challenge 1")
    stop_event.set()