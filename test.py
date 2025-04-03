import pyautogui
import speech_recognition as sr

def listen_for_open():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        print("🎤 Say 'open' to trigger double click...")

    while True:
        try:
            with mic as source:
                audio = recognizer.listen(source, timeout=5)
                command = recognizer.recognize_google(audio).lower()
                print("Heard:", command)

                if "open" in command:
                    print("🟢 Double clicking...")
                    pyautogui.doubleClick()
        except Exception as e:
            print("Error:", e)

listen_for_open()
