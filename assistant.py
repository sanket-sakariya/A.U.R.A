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
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

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
        recognizer.adjust_for_ambient_noise(source, duration=0.3)
        audio = recognizer.listen(source, phrase_time_limit=10)
    try:
        if update_status:
            update_status("Recognizing...")
        query = recognizer.recognize_google(audio, language='en-in')
        if update_output:
            update_output(f"You: {query}")
        return query.lower()
    except sr.UnknownValueError:
        if update_output:
            update_output("Sorry, I didn't catch that.")
    except sr.RequestError:
        if update_output:
            update_output("Speech service unavailable.")
    return "none"


def start_screen_recording(update_status=None, update_output=None):
    global recording, out
    if recording:
        speak("Recording is already in progress.", update_status, update_output)
        return

    recording = True
    screen_size = pyautogui.size()
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
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
    speak("Good day. I am Aura, your Autonomous User Response Assistant. At your service, always.", update_status, update_output)


def process_text_command(query, update_status, update_output):
    """Process text commands (same logic as voice commands)"""
    query = query.lower()
    
    if query in ['exit', 'quit', 'stop assistant', 'close assistant']:
        speak("Goodbye!", update_status, update_output)
        return "exit"

    elif "open" in query:
        from openapp import open_app
        app_name = query.replace("open", "").strip()
        open_app(app_name, update_status, update_output)

    elif "create" in query and "file" in query:
        from file import create_and_write_file
        filename = create_and_write_file(query, update_status, update_output)
        if filename:
            update_status("Waiting for next instruction to write content...")

    elif "read" in query or "show content" in query:
        from file import read_created_file
        read_created_file(query, update_status, update_output)

    elif "close" in query:
        from openapp import close_app
        app_name = query.replace("close", "").strip()
        close_app(app_name, update_status, update_output)

    elif "minimize" in query or "small" in query:
        from openapp import minimize_app
        app_name = query.replace("minimize", "").replace("small", "").strip()
        minimize_app(app_name, update_status, update_output)

    elif "maximize" in query or "big" in query:
        from openapp import maximize_app
        app_name = query.replace("maximize", "").replace("big", "").strip()
        maximize_app(app_name, update_status, update_output)

    elif "play" in query.lower() and "youtube" in query.lower():
        from webcontrol import play_youtube_video
        play_youtube_video(query, update_status, update_output)

    elif "weather" in query.lower():
        from webcontrol import get_weather
        import re
        match = re.search(r"(?:weather in|weather at|in|at)\s+(.*)", query)
        city = match.group(1).strip() if match else "Rajkot"
        weather_info = get_weather(city)
        update_status("Fetching weather information...")
        speak(weather_info, update_status, update_output)
        update_output(weather_info)

    elif "website" in query:
        from webcontrol import open_website, close_website
        command = query.lower().strip()
        if "stop website" in command:
            close_website(command, update_status, update_output)
        elif "start website" in command:
            open_website(command, update_status, update_output)
        else:
            update_output("Please say 'open website [name]' or 'close website [name]'.")

    elif "lock pc" in query:
        from openapp import lock_pc
        lock_pc(update_status, update_output)

    elif 'wikipedia' in query:
        speak("Searching Wikipedia...", update_status, update_output)
        try:
            results = wikipedia.summary(query.replace("wikipedia", ""), sentences=4)
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

    elif 'start' in query.lower() and 'recording' in query.lower():
        speak("Starting screen recording", update_status, update_output)
        start_screen_recording(update_status, update_output)

    elif 'stop' in query.lower() and 'recording' in query.lower():
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

    elif "summarize" in query.lower() or "summary" in query.lower():
        from gemini_chat import summarize_document
        import re
        
        # Extract file path from command
        # Patterns: "summarize file.pdf", "summary of document.docx", "read and summarize report.pdf"
        patterns = [
            r"summarize\s+(.+?)(?:\s|$)",
            r"summary\s+(?:of\s+)?(.+?)(?:\s|$)",
            r"read\s+(?:and\s+)?summarize\s+(.+?)(?:\s|$)",
            r"summarize\s+(?:the\s+)?(?:file\s+)?(.+?)(?:\s|$)"
        ]
        
        file_path = None
        for pattern in patterns:
            match = re.search(pattern, query.lower())
            if match:
                file_path = match.group(1).strip()
                break
        
        if not file_path:
            speak("Please specify the file you want me to summarize. For example: 'summarize document.pdf' or 'summary of report.docx'", update_status, update_output)
            return "continue"
        
        # Check if file exists
        if not os.path.exists(file_path):
            # Try looking in current directory
            current_dir_files = [f for f in os.listdir('.') if os.path.isfile(f)]
            matching_files = [f for f in current_dir_files if file_path.lower() in f.lower()]
            
            if matching_files:
                file_path = matching_files[0]
                speak(f"Found file: {file_path}", update_status, update_output)
            else:
                speak(f"File '{file_path}' not found. Please check the file name and try again.", update_status, update_output)
                return "continue"
        
        # Check file extension
        file_extension = os.path.splitext(file_path)[1].lower()
        if file_extension not in ['.pdf', '.docx', '.doc']:
            speak(f"Unsupported file format '{file_extension}'. I can only summarize PDF (.pdf) and Word (.docx, .doc) documents.", update_status, update_output)
            return "continue"
        
        # Process the document
        speak(f"Starting to summarize {os.path.basename(file_path)}...", update_status, update_output)
        summary = summarize_document(file_path, update_status, update_output)
        
        if summary.startswith("Error:"):
            speak(summary, update_status, update_output)
        else:
            # Split summary into smaller parts for speech
            summary_parts = summary.split('\n\n')
            for part in summary_parts:
                if part.strip():
                    speak(part.strip(), update_status, update_output)
                    update_output(part.strip())

    else:
        prompt = query.strip()
        from gemini_chat import ask_gemini
        response = ask_gemini(prompt)
        speak(response, update_status, update_output)
    
    return "continue"


def run_assistant(update_status, update_output, close_app_callback, set_text_callback=None):
    greet(update_status, update_output)
    
    # Set up text command callback if provided
    if set_text_callback:
        def text_command_handler(text):
            return process_text_command(text, update_status, update_output)
        set_text_callback(text_command_handler)
    
    while True:
        query = take_command(update_status, update_output)
        if query == "none":
            continue

        result = process_text_command(query, update_status, update_output)
        if result == "exit":
            close_app_callback()
            break