import struct
import threading
import socket
import time
import pickle
import cv2

from camera import camera_functions as cf

net_data = b""
header_size = struct.calcsize("!Qb")  # 8 bytes for size, 1 byte for key
send_buffer = b""

stop_event = threading.Event()
send_lock = threading.Lock()
connection_alive = True  # Track connection state
connection_lock = threading.Lock()  # Lock for connection state

"""
functions to parse different payload types based on data key
key = 1 for video frame, key = 2 for sensor data, key = 3 for controller data
"""

image_data = cv2.imread('0.png') # for video frame data
def parse_image_data(data):
    global image_data
    image_data = cf.decode_frame_bytes_jpeg(data)

def get_image_data():
    return image_data


sensor_data = None # for sensor data
sensor_lock = threading.Lock()
def parse_sensor_data(data):
    global sensor_data
    with sensor_lock:
        # Parse your sensor data here
        sensor_data = data

def get_sensor_data():
    with sensor_lock:
        return sensor_data


controller_data = []
controller_lock = threading.Lock()
def parse_controller_data(data): # for xbox controller data
    global controller_data
    with controller_lock:
        # Parse controller data here
        controller_data = data

def get_controller_data():
    with controller_lock:
        return controller_data

"""
Network thread functions
"""

def add_to_send_buffer(data, key):
    """Add data to send buffer - called from main thread"""
    if not connection_alive:
        return False

    global send_buffer
    header = struct.pack("!Qb", len(data), key)
    with send_lock:
        send_buffer += header + data
    return True


def receiver_thread(client_socket):
    """Dedicated thread for receiving data"""
    print("Receiver thread started")
    global net_data, connection_alive

    client_socket.settimeout(0.5)
    header_was_read = False
    msg_size = 0
    key = 0

    while not stop_event.is_set() and connection_alive:
        try:
            chunk = client_socket.recv(4 * 1024)
            if not chunk:
                print("Socket closed by peer (empty chunk)")
                connection_alive = False
                break
            net_data += chunk
        except socket.timeout:
            # Timeout is normal, continue to check stop_event
            continue
        except Exception as e:
            print(f"Error receiving data: {e}")
            with connection_lock:
                connection_alive = False
            break

        # Process all complete messages in the buffer
        while True:
            if not header_was_read:
                if len(net_data) < header_size:
                    break
                msg_size, key = struct.unpack("!Qb", net_data[:header_size])
                net_data = net_data[header_size:]
                header_was_read = True

            if len(net_data) < msg_size:
                break

            msg_data = net_data[:msg_size]
            net_data = net_data[msg_size:]

            if key == 1:
                parse_image_data(msg_data)
            elif key == 2:
                parse_sensor_data(msg_data)
            elif key == 3:
                parse_controller_data(msg_data)
            else:
                print(f"Unknown data key: {key}, ignoring message")

            header_was_read = False

    print("Receiver thread exiting")


def sender_thread(client_socket):
    """Dedicated thread for sending data"""
    print("Sender thread started")
    global send_buffer, connection_alive

    while not stop_event.is_set() and connection_alive:
        # Check if there's data to send
        if send_buffer:
            with send_lock:
                to_send = send_buffer
                send_buffer = b""

            try:
                client_socket.sendall(to_send)
                # print(f"Sent {len(to_send)} bytes")
            except Exception as e:
                print(f"Error sending data: {e}")
                with connection_lock:
                    connection_alive = False
                break
        else:
            # No data to send, sleep briefly to prevent CPU spinning
            # Use a short sleep that can be interrupted by stop_event
            time.sleep(0.001)  # 1ms sleep is enough

    print("Sender thread exiting")


def stop_network_thread():
    """Signal all network threads to stop"""
    print("Stopping network threads...")
    stop_event.set()


def network_tread(client_socket):
    """Main network thread that spawns sender and receiver"""
    print("Starting network threads")

    # Clear any previous stop event
    stop_event.clear()

    # Start sender and receiver threads
    sender = threading.Thread(target=sender_thread, args=(client_socket,), daemon=True)
    receiver = threading.Thread(target=receiver_thread, args=(client_socket,), daemon=True)

    sender.start()
    receiver.start()

    # Monitor threads and stop_event
    while not stop_event.is_set():
        # Check if either thread died
        if not sender.is_alive() or not receiver.is_alive():
            print("A network thread died, stopping...")
            break

        # Short sleep to prevent CPU spinning
        time.sleep(0.1)

    # Signal stop to all threads
    stop_event.set()

    # Wait for threads to finish with timeout
    sender.join(timeout=2)
    receiver.join(timeout=2)

    # Force close socket if threads are still alive
    if sender.is_alive() or receiver.is_alive():
        print("Force closing socket to unblock threads")
        try:
            client_socket.close()
        except:
            pass

    print("Network thread exiting")