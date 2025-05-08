import datetime
import os
import pyautogui
import pyttsx3
import speech_recognition as sr
import pywhatkit
import wikipedia
import cv2
import numpy as np
from threading import Thread

recognizer = sr.Recognizer()
engine = pyttsx3.init()

recording = False
out = None


def speak(text, update_status=None, update_output=None):
    if update_status:
        update_status("Speaking...")
    if update_output:
        update_output(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()
    if update_status:
        update_status("Idle")

def take_command(update_status=None, update_output=None):
    with sr.Microphone() as source:
        if update_status:
            update_status("Listening...")
        recognizer.pause_threshold = 1
        audio = recognizer.listen(source)
    try:
        if update_status:
            update_status("Recognizing...")
        query = recognizer.recognize_google(audio, language='en-in')
        if update_output:
            update_output(f"You: {query}")
        return query.lower()
    except:
        if update_output:
            update_output("Didn't catch that.")
        return "none"

def start_screen_recording(update_status=None, update_output=None):
    global recording, out
    if recording:
        speak("Recording is already in progress.", update_status, update_output)
        return

    recording = True
    screen_size = pyautogui.size()
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    filename = f"screen_record_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.avi"
    out = cv2.VideoWriter(filename, fourcc, 10.0, screen_size)

    def record():
        global recording
        while recording:
            img = pyautogui.screenshot()
            frame = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)
            out.write(frame)
        out.release()
        speak("Screen recording saved", update_status, update_output)

    Thread(target=record).start()

def stop_screen_recording(update_status=None, update_output=None):
    global recording
    if recording:
        recording = False
        speak("Recording has been stopped.", update_status, update_output)
    else:
        speak("No recording is currently active.", update_status, update_output)


def greet(update_status, update_output):
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        greet_msg = "Good Morning!"
    elif 12 <= hour < 18:
        greet_msg = "Good Afternoon!"
    else:
        greet_msg = "Good Evening!"
    speak(greet_msg, update_status, update_output)
    speak("I am your futuristic assistant. How can I help you?", update_status, update_output)

def run_assistant(update_status, update_output, close_app_callback):
    greet(update_status, update_output)
    while True:
        query = take_command(update_status, update_output)
        if query == "none":
            continue

        if query in ['exit', 'quit', 'stop assistant', 'close assistant']:
            speak("Goodbye!", update_status, update_output)
            listening = False
            close_app_callback()
            break
        elif "open" in query:
            from openapp import open_app
            app_name = query.replace("open", "").strip()
            open_app(app_name, update_status, update_output)

        elif "close" in query:
            from openapp import close_app
            app_name = query.replace("close", "").strip()
            close_app(app_name, update_status, update_output)

        elif 'open youtube' in query:
            speak("Opening YouTube", update_status, update_output)
            pywhatkit.playonyt("latest songs")

        elif 'open google' in query:
            speak("Opening Google", update_status, update_output)
            pywhatkit.search("Google")

        elif 'wikipedia' in query:
            speak("Searching Wikipedia...", update_status, update_output)
            try:
                results = wikipedia.summary(query.replace("wikipedia", ""), sentences=2)
                speak("According to Wikipedia", update_status, update_output)
                speak(results, update_status, update_output)
            except:
                speak("Couldn't find results.", update_status, update_output)

        elif 'time' in query:
            speak(datetime.datetime.now().strftime("%I:%M %p"), update_status, update_output)

        elif 'date' in query:
            speak(datetime.datetime.now().strftime("%B %d, %Y"), update_status, update_output)

        elif 'screenshot' in query:
            filename = f"screenshot_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            pyautogui.screenshot().save(filename)
            speak("Screenshot taken", update_status, update_output)

        elif 'increase brightness' in query:
            os.system("powershell (Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,80)")
            speak("Increasing brightness", update_status, update_output)

        elif 'decrease brightness' in query:
            os.system("powershell (Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,30)")
            speak("Decreasing brightness", update_status, update_output)

        elif 'increase volume' in query:
            pyautogui.press("volumeup")
            speak("Increasing volume", update_status, update_output)

        elif 'decrease volume' in query:
            pyautogui.press("volumedown")
            speak("Decreasing volume", update_status, update_output)

        elif 'mute volume' in query:
            pyautogui.press("volumemute")
            speak("Volume muted", update_status, update_output)

        elif 'start recording' in query:
            speak("Starting screen recording", update_status, update_output)
            start_screen_recording(update_status, update_output)

        elif 'stop recording' in query:
            speak("Stopping screen recording", update_status, update_output)
            stop_screen_recording(update_status, update_output)

        elif 'search' in query:
            search_query = query.replace("search", "").strip()
            speak(f"Searching for {search_query}", update_status, update_output)
            pywhatkit.search(search_query)
            
        elif "gemini" in query:
            prompt = query.replace("gemini", "").strip()
            from gemini_chat import ask_gemini
            response = ask_gemini(prompt)
            speak(response, update_status, update_output)

        else:
            prompt = query.strip()
            from gemini_chat import ask_gemini
            response = ask_gemini(prompt)
            speak(response, update_status, update_output)
