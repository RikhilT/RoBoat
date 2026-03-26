import threading
import time
from math import floor

import networking
import serial
import math
stop_event = threading.Event()

def start():
    # print("Starting Manual Control")
    # SerialObj = serial.Serial('COM7', 9600, 8)  # , 'N', 1
    time.sleep(1)
    deadzone = 3000
    scale_factor = 255 / 32767
    while not stop_event.is_set():
        state = networking.get_controller_data()
        RY = int(state['sThumbRY'])
        RY = RY if abs(RY) >= deadzone else 0
        RX = int(state['sThumbRX'])
        RX = RX if abs(RX) >= deadzone else 0

        RY = int(RY * scale_factor)
        RX = int(RX * scale_factor)

        print(f"RY: {RY}, RX: {RX}")


        to_send = RY.to_bytes(2, 'big', signed=True) + RX.to_bytes(2, 'big', signed=True)
        # SerialObj.write(to_send)

        time.sleep(0.2)

def stop():
    print("Stopping Manual Control")
    stop_event.set()