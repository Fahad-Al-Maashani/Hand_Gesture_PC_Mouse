import cv2
import mediapipe as mp
import pyautogui
import math
import time
import threading
import speech_recognition as sr

# Initialize MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7
)
mp_draw = mp.solutions.drawing_utils

# Screen dimensions
screen_width, screen_height = pyautogui.size()

# Webcam
cap = cv2.VideoCapture(0)

# Smoothing
prev_x, prev_y = 0, 0
smooth_factor = 0.2  # Change between 0.1 (very smooth) and 0.3 (more responsive)

# Click logic
click_start_time = None
clicking = False
click_cooldown = 1
last_click_time = 0
magnet_enabled = True

# Gesture zones
zones = {
    "TOP_LEFT": (0, 0, screen_width // 4, screen_height // 4),
    "TOP_RIGHT": (screen_width * 3 // 4, 0, screen_width // 4, screen_height // 4),
    "BOTTOM_RIGHT": (screen_width * 3 // 4, screen_height * 3 // 4, screen_width // 4, screen_height // 4),
}

# Helper functions
def distance(p1, p2):
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])

def in_zone(x, y, zone):
    zx, zy, zw, zh = zone
    return zx <= x <= zx + zw and zy <= y <= zy + zh

def lerp(a, b, f):
    return a + (b - a) * f

# 🎤 Voice Listener for "open"
def listen_for_voice():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)

    while True:
        try:
            with mic as source:
                print("🎤 Listening for 'open'...")
                audio = recognizer.listen(source, timeout=5)
                command = recognizer.recognize_google(audio).lower()
                print("🗣 You said:", command)

                if "open" in command or "open folder" in command:
                    print("✅ Triggering double click...")
                    pyautogui.doubleClick()
        except Exception as e:
            print("Voice Error:", e)

# Start voice thread
voice_thread = threading.Thread(target=listen_for_voice, daemon=True)
voice_thread.start()

# Main loop
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)
    frame_height, frame_width, _ = frame.shape

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Get fingertip positions
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]

            x_index = int(index_tip.x * frame_width)
            y_index = int(index_tip.y * frame_height)
            x_thumb = int(thumb_tip.x * frame_width)
            y_thumb = int(thumb_tip.y * frame_height)

            dist = distance((x_index, y_index), (x_thumb, y_thumb))
            screen_x = int(x_index * screen_width / frame_width)
            screen_y = int(y_index * screen_height / frame_height)

            # Gesture zones
            for name, zone in zones.items():
                if in_zone(screen_x, screen_y, zone):
                    cv2.putText(frame, f"Zone: {name}", (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
                    if name == "TOP_LEFT":
                        pyautogui.press('volumeup')
                    elif name == "TOP_RIGHT":
                        pyautogui.hotkey('ctrl', 't')
                    elif name == "BOTTOM_RIGHT":
                        pyautogui.hotkey('alt', 'f4')

            # Magnet snap (demo)
            center_x, center_y = screen_width // 2, screen_height // 2
            if magnet_enabled and abs(screen_x - center_x) < 50 and abs(screen_y - center_y) < 50:
                pyautogui.moveTo(center_x, center_y)
                cv2.putText(frame, "MAGNET SNAP", (x_index, y_index - 40),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)
            else:
                curr_x = lerp(prev_x, screen_x, smooth_factor)
                curr_y = lerp(prev_y, screen_y, smooth_factor)
                if abs(curr_x - prev_x) > 2 or abs(curr_y - prev_y) > 2:
                    pyautogui.moveTo(curr_x, curr_y)
                    prev_x, prev_y = curr_x, curr_y

            # Click / Hold
            if dist < 40:
                if click_start_time is None:
                    click_start_time = time.time()
                elapsed = time.time() - click_start_time
                if elapsed > 1.0 and not clicking:
                    pyautogui.mouseDown()
                    clicking = True
                    cv2.putText(frame, "HOLDING", (x_index, y_index - 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                elif not clicking:
                    cv2.putText(frame, "CLICK READY", (x_index, y_index - 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
            else:
                if clicking:
                    pyautogui.mouseUp()
                    clicking = False
                    click_start_time = None
                elif click_start_time is not None:
                    if time.time() - click_start_time < 1.0 and time.time() - last_click_time > click_cooldown:
                        pyautogui.click()
                        last_click_time = time.time()
                        cv2.putText(frame, "CLICK", (x_index, y_index - 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    click_start_time = None

            # Draw finger circles
            cv2.circle(frame, (x_index, y_index), 10, (255, 0, 0), -1)
            cv2.circle(frame, (x_thumb, y_thumb), 10, (0, 255, 0), -1)

    # Draw zones
    for z in zones.values():
        x, y, w, h = z
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255), 1)

    # Display frame
    cv2.imshow("🖐️ Gesture + Voice Mouse Control", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
