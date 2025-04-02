# 🖐️🧠 Gesture & Voice Controlled Mouse System

Control your computer like Tony Stark — using only your **hand gestures** and **voice**!  
This project combines **MediaPipe** hand tracking with **offline voice commands** using **VOSK**, creating a smart, futuristic interface for hands-free PC control.

---

## 🚀 Features

| Feature         | Description                                                 |
|----------------|-------------------------------------------------------------|
| 👆 Cursor Move  | Move your index finger to move the mouse pointer           |
| 👌 Click        | Tap thumb + index to perform a click                       |
| ✊ Click & Hold | Hold the gesture for >1s to perform a mouse hold           |
| 🧲 Magnet Snap  | Cursor auto-snaps to center screen if close (demo)        |
| 🧭 Zones        | Custom screen areas trigger actions like volume & closing |
| 🗣 Voice Cmd    | Say "**open**" to open folder under your cursor (offline)  |

---

## 📷 Preview

_> Add a screenshot or a GIF showing hand and voice in action._

---

## 🔧 Installation

### ✅ Clone the Repo

```bash
git clone https://github.com/yourusername/gesture-voice-mouse-control.git
cd gesture-voice-mouse-control
```

### ✅ Create a Virtual Environment (Optional)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### ✅ Install Dependencies

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install opencv-python mediapipe pyautogui speechrecognition pyaudio vosk sounddevice pyttsx3
```

### ✅ Download VOSK Offline Model

```bash
wget https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip
unzip vosk-model-small-en-us-0.15.zip
mv vosk-model-small-en-us-0.15 vosk-model
```

Or [download manually](https://alphacephei.com/vosk/models) and extract it into a folder named `vosk-model`.

---

## 🧠 How to Use

### Step 1: Run the Gesture Controller

```bash
python main.py
```

### Step 2: Run the Voice Command Listener

```bash
python voice_command.py
```

### Step 3: Try It Out!

- Move your hand to control the cursor
- Touch thumb + index to click
- Say **"open"** to open the folder under your cursor

---

## 📁 Project Structure

```
gesture-voice-mouse-control/
├── main.py             # Hand gesture mouse control
├── voice_command.py    # Listens for voice commands ("open")
├── vosk-model/         # Offline speech model directory
├── requirements.txt    # Dependencies
└── README.md           # Project documentation
```

---

## 💡 Tips

- Use in a well-lit area for better hand tracking
- Ensure microphone permissions are enabled
- Works offline — no internet required for speech recognition

---

## 🤖 Built With

- [MediaPipe](https://mediapipe.dev/) – Real-time hand tracking
- [OpenCV](https://opencv.org/) – Webcam interface
- [PyAutoGUI](https://pyautogui.readthedocs.io/) – Mouse automation
- [VOSK](https://alphacephei.com/vosk/) – Offline voice recognition
- [SpeechRecognition](https://pypi.org/project/SpeechRecognition/) – Voice parsing

---

## 📜 License

MIT License – free to use, modify, and share.

---

## 🙌 Author

**Fahad Al Maashani**  
Building the future of natural human-computer interaction ✨
