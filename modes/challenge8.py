import threading
import time
stop_event = threading.Event()

def start():
    print("Starting Challenge 8")

    while not stop_event.is_set():
        print("Doing Challenge 8")
        time.sleep(0.5)
        pass

def stop():
    print("Stopping Challenge 8")
    stop_event.set()