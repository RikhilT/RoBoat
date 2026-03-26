import cv2
from ultralytics import YOLO
import numpy as np

model = YOLO('best.pt')

results = model.predict("Test_Images/buoy_1.jpg", device='cpu')
print(model.names)
color_vals = [
    (0, 0, 255),
    (0, 255, 0),
    (255, 0, 0),
    (0, 165, 255),
    (147, 20, 255),
    (0, 255, 255),
    (255, 255, 255),
    (0, 0, 0)
]

for result in results:
    boxes = result.boxes
    img = result.orig_img.copy()

    for box in boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        confidence = float(box.conf[0].item())
        if confidence < 0.7:
            continue
        class_id = int(box.cls[0].item())
        label = f"{model.names[class_id]} {confidence:.2f}"
        cv2.rectangle(img, (x1, y1), (x2, y2), color_vals[class_id], 2)
        # cv2.putText(img, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color_vals[class_id], 2)
        print(f"Object: {model.names[class_id]}, Box: {x1, y1, x2, y2}, Confidence: {confidence}")

    # resize image to half its size before displaying
    h, w = img.shape[:2]
    img = cv2.resize(img, (w // 3, h // 3), interpolation=cv2.INTER_AREA)
    cv2.imshow("Predictions", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.imwrite("predicted_image.png", img)
