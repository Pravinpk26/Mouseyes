import cv2
import numpy as np
from PIL import Image
import time

def show_pixel_value(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE:
        hsv_pixel = hsvImage[y, x]
        print(f"HSV at ({x},{y}): {hsv_pixel}")

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Camera not accessible")
    exit()

snapshot_taken = False

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lowerLimit = np.array([20, 100, 100])
    upperLimit = np.array([40, 255, 255])

    mask = cv2.inRange(hsvImage, lowerLimit, upperLimit)
    cv2.imshow("mask", mask)

    mask_ = Image.fromarray(mask)
    bbox = mask_.getbbox()

    if bbox is not None:
        x1, y1, x2, y2 = bbox
        frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 5)

        if not snapshot_taken:
            timestamp = time.strftime("%Y%m%d-%H%M%S")

            # Save color (BGR) frame
            color_filename = f"snapshot_color_{timestamp}.png"
            cv2.imwrite(color_filename, frame)

            # Save HSV (converted to BGR)
            hsv_bgr = cv2.cvtColor(hsvImage, cv2.COLOR_HSV2BGR)
            hsv_filename = f"snapshot_hsv_{timestamp}.png"
            cv2.imwrite(hsv_filename, hsv_bgr)

            # Save the binary mask
            mask_filename = f"snapshot_mask_{timestamp}.png"
            cv2.imwrite(mask_filename, mask)

            print(f"Saved: {color_filename}, {hsv_filename}, {mask_filename}")
            snapshot_taken = True
    else:
        snapshot_taken = False

    cv2.imshow("frame", frame)
    cv2.setMouseCallback("frame", show_pixel_value)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
