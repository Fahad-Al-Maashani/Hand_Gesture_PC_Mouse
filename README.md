# Hand_Gesture_PC_Mouse
This repo will be about writing a simple program that uses hands to control the computer instead of mouse. 
The idea behind this is to control your mouse cursor using hand gestures captured from a webcam feed. It uses **MediaPipe** for real-time hand tracking, **OpenCV** for video processing, and **PyAutoGUI** for mouse control.
## Features
- Detects hand gestures in real time using your webcam.
- Tracks the movement of your index finger to control the mouse cursor.
- Maps hand positions from the camera feed to screen coordinates.

## Requirements
- Python 3.8 or higher
- Libraries:
  - OpenCV: `pip install opencv-python`
  - MediaPipe: `pip install mediapipe`
  - PyAutoGUI: `pip install pyautogui`

## How It Works
1. **Hand Tracking**:
   - MediaPipe detects hand landmarks from the webcam feed.
   - The position of the index finger (landmark 8) is extracted.

2. **Screen Mapping**:
   - The coordinates of the index finger from the camera feed are mapped to your screen dimensions.

3. **Mouse Control**:
   - PyAutoGUI moves the mouse cursor to the mapped coordinates.

## Setup Instructions
1. Clone the project repository:
   ```bash
   git clone https://github.com/YourUsername/Hand-Gesture-Mouse-Control.git
