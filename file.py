import os
from assistant import speak
from gemini_chat import ask_gemini

def create_and_write_file(command, update_status=None, update_output=None):
    try:
        # Extract filename and extension
        words = command.lower().split()
        if "file" in words and "name" in words:
            ext = next((w for w in words if w in ["text", "python", "html", "java", "json"]), "text")
            name_index = words.index("name") + 1
            filename = words[name_index]
            extension = {
                "text": ".txt",
                "python": ".py",
                "html": ".html",
                "java": ".java",
                "json": ".json"
            }.get(ext, ".txt")

            full_filename = f"{filename}{extension}"

            # Extract prompt for Gemini after 'named <filename>'
            prompt_start_index = command.lower().find(filename) + len(filename)
            prompt = command[prompt_start_index:].strip()

            # Ask Gemini and write content
            content = ask_gemini(prompt)
            with open(full_filename, "w", encoding="utf-8") as f:
                f.write(content)

            if update_status:
                update_status(f"Created and written to {full_filename}")
            if update_output:
                update_output(f"File `{full_filename}` created and content written successfully.")

            return full_filename

    except Exception as e:
        if update_output:
            update_output(f"Error: {e}")
        return None


# "Create a {extension} file name {file_name} that calculates factorial of a number"


def read_created_file(command, update_status=None, update_output=None):
    try:
        # Extract file extension and filename
        words = command.lower().split()
        if "file" in words and "name" in words:
            ext = next((w for w in words if w in ["text", "python", "html", "java", "json"]), "text")
            name_index = words.index("name") + 1
            filename = words[name_index]

            extension = {
                "text": ".txt",
                "python": ".py",
                "html": ".html",
                "java": ".java",
                "json": ".json"
            }.get(ext, ".txt")

            full_filename = f"{filename}{extension}"

            if not os.path.exists(full_filename):
                msg = f"File '{full_filename}' does not exist."
                if update_output:
                    update_output(msg)
                if update_status:
                    update_status("File not found")
                speak("Sorry, I couldn't find the file.")
                return

            with open(full_filename, "r", encoding="utf-8") as f:
                content = f.read()

            if update_status:
                update_status(f"Reading {full_filename}")
            if update_output:
                update_output(f"Content of `{full_filename}`:\n\n{content}")
            speak(f"Here is the content of {full_filename}")
            speak(content[:400])  # Speak only first 400 chars to avoid overload

            return content

    except Exception as e:
        if update_output:
            update_output(f"Error: {e}")
        speak("Something went wrong while reading the file.")
        return None



# “Read file name demo”

# “Open and read python file name script”

# “Show content of html file name index”