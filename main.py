import socket, pickle, struct, serial, threading
import cv2
import time
import networking
import numpy as np
import mode_switcher

from PyQt6.QtWidgets import QApplication
from Client_GUI import MainWindow
import sys

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Connecting...")
# client_socket.connect(('localhost', 54321))
# client_socket.connect(('192.168.1.5', 54321))
client_socket.connect(('10.42.0.1', 54321))
print("Connected!")

thread_network = threading.Thread(target=networking.network_tread, args=(client_socket,))
thread_network.start()

app = QApplication(sys.argv)
w = MainWindow()
w.show()

manual_control = threading.Thread(target=mode_switcher.manual_control_thread, daemon=True)
manual_control.start()

exit_code = app.exec()
w.stop_timer()
networking.stop_network_thread()
mode_switcher.stop_manual_control_thread()
time.sleep(1) # wait for the threads to stop
if client_socket:
    try:
        client_socket.shutdown(socket.SHUT_RDWR)
        client_socket.close()
    except:
        pass

print("Sockets closed, exiting program")
sys.exit(exit_code)