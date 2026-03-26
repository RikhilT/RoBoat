import cv2
import pickle

cap = cv2.VideoCapture(0)
def get_frame_bytes_jpeg(quality=80):
    global cap
    ret, frame = cap.read()
    if not ret:
        return None

    _, cvimage = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, quality])
    return pickle.dumps(cvimage)

    # return pickle.dumps(frame)

def release_camera():
    global cap
    cap.release()