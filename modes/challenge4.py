import threading
import time
stop_event = threading.Event()

def start():
    print("Starting Challenge 4")

    while not stop_event.is_set():
        print("Doing Challenge 4")
        time.sleep(0.5)
        pass

def stop():
    print("Stopping Challenge 4")
    stop_event.set()