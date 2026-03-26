import threading
import time
stop_event = threading.Event()

def start():
    print("Running Nothing")

    while not stop_event.is_set():
        print("Doing Nothing")
        time.sleep(0.5)
        pass

def stop():
    print("Stopping Nothing")
    stop_event.set()