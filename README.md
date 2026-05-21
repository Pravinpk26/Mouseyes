# 👁️ Mouseyes

> Control your mouse with just your eyes — a hands-free, accessibility-first input system built with OpenCV and MediaPipe.

---

## 🧠 About

Mouseyes is a real-time eye-tracking mouse controller. It uses your webcam to track iris position via MediaPipe's Face Mesh, maps gaze direction to screen coordinates, and translates blinks into clicks and drag actions — no hardware beyond a standard webcam required.

Designed to promote accessibility and hands-free computing for users with limited mobility.

---

## ✨ Features

- **Gaze-based cursor movement** — iris position mapped to full screen with smoothing
- **Calibration** — press `C` while looking at screen center to set your gaze reference point
- **Blink to click** — short blink triggers a mouse click
- **Blink to drag** — hold blink for 1.5s to start dragging; release blink to drop
- **Adjustable sensitivity** — tweak `blink_threshold` and `drag_time_required` in code
- **Live preview window** — shows iris tracking dot overlaid on webcam feed

---

## 🗂️ Project Structure

```
Mouseyes/
└── util.py    # Full eye-tracking + mouse control logic
```

---

## 🚀 Setup & Run

### Prerequisites
- Python 3.8+
- Webcam

### Install dependencies

```bash
pip install opencv-python mediapipe pyautogui
```

### Run

```bash
python util.py
```

### Controls

| Action | Trigger |
|---|---|
| Calibrate | Press `C` while looking at screen center |
| Move cursor | Move your eyes / gaze direction |
| Click | Short blink |
| Drag | Hold blink for 1.5 seconds |
| Release drag | Open eye |
| Exit | Press `ESC` |

---

## ⚙️ Configuration

Inside `util.py`, tune these variables to your environment:

```python
blink_threshold = 0.008   # Lower = more sensitive to blinks
drag_time_required = 1.5  # Seconds of closed eye to trigger drag
# Gaze sensitivity multiplier (line ~55):
dx = (iris_x - ref_x) * screen_w * 7   # Increase 7 for faster movement
```

---

## 🔧 How It Works

1. **Face Mesh** — MediaPipe detects 478 facial landmarks per frame
2. **Iris detection** — Landmarks 474–477 (right iris ring) are averaged to get gaze point
3. **Calibration** — On `C` press, current iris position is stored as the screen center reference
4. **Cursor mapping** — Delta from reference × sensitivity × screen size → screen coordinates
5. **Smoothing** — Exponential moving average prevents jitter
6. **Blink detection** — Vertical distance between landmarks 159 and 145 (left eyelid) compared against threshold

---

## 🛠️ Tech Stack

| Layer | Tool |
|---|---|
| Language | Python |
| Computer Vision | OpenCV (`cv2`) |
| Face/Iris Tracking | MediaPipe Face Mesh |
| Mouse Control | PyAutoGUI |

---

## 📄 License

Open source — free to use and modify.

---

*Built by [Pravin Kumar M](https://github.com/Pravinpk26)*
