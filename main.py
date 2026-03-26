import socket
import time
import threading
import networking
from camera import webcam

# Create Socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip = 'localhost'  # Localhost for testing on same machine
port = 54321
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((ip, port))

# Wait until someone connects to the socket
server_socket.listen(5)
print(f"LISTENING AT: {ip}:{port}")
client_socket, addr = server_socket.accept()
print('GOT CONNECTION FROM:', addr)

# Start network thread (this spawns sender and receiver threads and returns)
thread_network = threading.Thread(target=networking.network_tread, args=(client_socket,))
thread_network.start()

# Main loop - now runs because network_tread runs in separate thread
try:
    while networking.is_connected():
        try:
            frame_bytes = webcam.get_frame_bytes_jpeg(quality=80)
            networking.add_to_send_buffer(frame_bytes, 1)  # Non-blocking
            time.sleep(0.02)  # 50 fps target
        except Exception as e:
            print(f"Error in main loop: {e}")
            break
except KeyboardInterrupt:
    print("\nKeyboard interrupt received")

print("Closing program and sockets")
webcam.release_camera()
networking.stop_network_thread()
time.sleep(1)  # Wait for network threads to finish

# Close client socket if it exists
if client_socket:
    try:
        client_socket.shutdown(socket.SHUT_RDWR)
        client_socket.close()
    except:
        pass

# Close server socket
if server_socket:
    try:
        server_socket.close()
    except:
        pass

print("Sockets closed")