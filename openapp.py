import subprocess
import os
import webbrowser
import sys
import pygetwindow as gw

# Mapping of common app names to their executable paths or commands
APP_COMMANDS = {
    "word": r"start winword",   # MS Word
    "excel": r"start excel",    # MS Excel
    "powerpoint": r"start powerpnt",  # MS PowerPoint
    "notepad": r"notepad",
    "chrome": r"start chrome",
    "edge": r"start msedge",
    "calculator": r"calc",
    "paint": r"mspaint",
    "cmd": r"start cmd",
    "file explorer": r"explorer",
    "vs code": r"code",  # Assumes VS Code is added to PATH
}


def open_app(app_name, update_status, update_output):
    app_name = app_name.lower()
    command = APP_COMMANDS.get(app_name)

    if command:
        try:
            update_status(f"Opening {app_name}...")
            subprocess.Popen(command, shell=True)
            update_output(f"✅ {app_name.title()} launched successfully.")
        except Exception as e:
            update_output(f"❌ Failed to open {app_name}: {e}")
    else:
        update_output(f"⚠️ I don't recognize the app: '{app_name}'")
        update_status("Idle")

def close_app(app_name, update_status, update_output):
    app_name = app_name.lower()
    
    # Mapping apps to their taskkill executable names
    APP_CLOSE_COMMANDS = {
        "word": "winword.exe",
        "excel": "excel.exe",
        "powerpoint": "powerpnt.exe",
        "notepad": "notepad.exe",
        "chrome": "chrome.exe",
        "edge": "msedge.exe",
        "calculator": "calc.exe",
        "paint": "mspmsn.exe",  # Might vary depending on the system
        "cmd": "cmd.exe",
        "vs code": "Code.exe"
    }

    app_exe = APP_CLOSE_COMMANDS.get(app_name)

    if app_exe:
        try:
            update_status(f"Closing {app_name}...")
            subprocess.Popen(f"taskkill /f /im {app_exe}", shell=True)
            update_output(f"✅ {app_name.title()} closed successfully.")
        except Exception as e:
            update_output(f"❌ Failed to close {app_name}: {e}")
    else:
        update_output(f"⚠️ I don't recognize the app: '{app_name}'")
        update_status("Idle")


def minimize_app(app_name, update_status, update_output):
    try:
        windows = gw.getWindowsWithTitle(app_name)
        if windows:
            for window in windows:
                if window.isMinimized == False:
                    window.minimize()
                    update_status(f"Minimizing {app_name}...")
                    update_output(f"✅ {app_name.title()} minimized.")
                else:
                    update_output(f"⚠️ {app_name.title()} is already minimized.")
        else:
            update_output(f"⚠️ No window found with the name: {app_name}")
    except Exception as e:
        update_output(f"❌ Failed to minimize {app_name}: {e}")
        update_status("Idle")

def maximize_app(app_name, update_status, update_output):
    try:
        windows = gw.getWindowsWithTitle(app_name)
        if windows:
            for window in windows:
                if window.isMaximized == False:
                    window.maximize()
                    update_status(f"Maximizing {app_name}...")
                    update_output(f"✅ {app_name.title()} maximized.")
                else:
                    update_output(f"⚠️ {app_name.title()} is already maximized.")
        else:
            update_output(f"⚠️ No window found with the name: {app_name}")
    except Exception as e:
        update_output(f"❌ Failed to maximize {app_name}: {e}")
        update_status("Idle")
