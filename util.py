import cv2
import mediapipe as mp
import pyautogui
import time

#setup
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
cam = cv2.VideoCapture(0)

screen_w, screen_h = pyautogui.size()
prev_x, prev_y = pyautogui.position()

#calib
calibrated = False
ref_x, ref_y = 0, 0

#blink
blink_start_time = None
dragging = False
blink_threshold = 0.008  # smaller = more sensitive
drag_time_required = 1.5  # seconds

print("Press 'C' to calibrate while looking at the center of the screen.")
print("Press ESC to exit.")

while True:
    success, image = cam.read()
    if not success:
        continue

    image = cv2.flip(image, 1)
    img_h, img_w, _ = image.shape
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    result = face_mesh.process(rgb_image)

    key = cv2.waitKey(1) & 0xFF

    if result.multi_face_landmarks:
        mesh_points = result.multi_face_landmarks[0].landmark

        #irispos
        iris_pts = [mesh_points[i] for i in [474, 475, 476, 477]]
        iris_x = sum(p.x for p in iris_pts) / 4
        iris_y = sum(p.y for p in iris_pts) / 4

        #dot
        cx, cy = int(iris_x * img_w), int(iris_y * img_h)
        cv2.circle(image, (cx, cy), 4, (0, 255, 0), -1)

        #Calib
        if key == ord('c'):
            ref_x, ref_y = iris_x, iris_y
            calibrated = True
            print("Calibrated at center!")

        if not calibrated:
            cv2.putText(image, "Press 'C' to calibrate", (30, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        if calibrated:
            #cursmove
            dx = (iris_x - ref_x) * screen_w * 7  # Increase for sensitivity
            dy = (iris_y - ref_y) * screen_h * 7
            smooth_x = prev_x + (dx - prev_x) / 3
            smooth_y = prev_y + (dy - prev_y) / 3
            pyautogui.moveTo(smooth_x, smooth_y)
            prev_x, prev_y = smooth_x, smooth_y

        #LEBlink
        left_top = mesh_points[159]
        left_bottom = mesh_points[145]
        blink_dist = abs(left_top.y - left_bottom.y)

        if blink_dist < blink_threshold:
            if blink_start_time is None:
                blink_start_time = time.time()
            elif not dragging and time.time() - blink_start_time > drag_time_required:
                pyautogui.mouseDown()
                dragging = True
                print("Started drag")
        else:
            if dragging:
                pyautogui.mouseUp()
                dragging = False
                print("Released drag")
            elif blink_start_time and time.time() - blink_start_time < drag_time_required:
                pyautogui.click()
                print("Click")
            blink_start_time = None

    cv2.imshow("Eye Controlled Mouse", image)

    if key == 27:
        break

cam.release()
cv2.destroyAllWindows()
