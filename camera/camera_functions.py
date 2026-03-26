import cv2
import pickle

def decode_frame_bytes_jpeg(frame_bytes):
    try:
        cvimage = pickle.loads(frame_bytes) # Still a bytes object representing the encoded JPEG image
        # frame = cv2.imdecode(cvimage, cv2.IMREAD_COLOR)
        frame = cvimage
        return frame
    except Exception as e:
        print(f"Error decoding frame bytes: {e}")
        return None