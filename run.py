import subprocess
import os
import sys
import signal

# Path to your actual GUI app
script_path = os.path.join(os.path.dirname(__file__), 'gui.py')

def launch_app():
    try:
        # Start the GUI app as a subprocess
        process = subprocess.Popen([sys.executable, script_path])
        print("A.U.R.A launched successfully.")

        # Wait for GUI to close
        process.wait()
        print("GUI exited. Cleaning up...")

        # Explicitly terminate the subprocess if still alive
        if process.poll() is None:
            process.terminate()
            process.wait(timeout=1)

    except KeyboardInterrupt:
        print("KeyboardInterrupt received. Closing NOVA...")
        process.terminate()
        process.wait()
    except Exception as e:
        print(f"Failed to launch or close NOVA: {e}")

if __name__ == "__main__":
    launch_app()
