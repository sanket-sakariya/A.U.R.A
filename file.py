import os
from assistant import speak
from gemini_chat import ask_gemini,code_gemini


def create_and_write_file(command, update_status=None, update_output=None):
    try:
        # Create output folder if it doesn't exist
        output_folder = "output"
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        
        # Extract filename and extension
        words = command.lower().split()
        if "file" in words and "name" in words:
            ext = next((w for w in words if w in ["text", "python", "html", "java", "json", "javascript", "php"]), "text")
            name_index = words.index("name") + 1
            filename = words[name_index]
            extension = {
                "text": ".txt",
                "python": ".py",
                "html": ".html",
                "java": ".java",
                "javascript": ".js",
                "php": ".php",
                "json": ".json"
            }.get(ext, ".txt")

            full_filename = f"{filename}{extension}"
            # Create full path with output folder
            file_path = os.path.join(output_folder, full_filename)

            # Extract prompt for Gemini after 'named <filename>'
            prompt_start_index = command.lower().find(filename) + len(filename)
            prompt = command[prompt_start_index:].strip()

            # Ask Gemini and write content
            content = code_gemini(prompt,extension)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)

            if update_status:
                update_status(f"Created and written to {file_path}")
            if update_output:
                update_output(f"File `{file_path}` created and content written successfully.")

            return file_path

    except Exception as e:
        if update_output:
            update_output(f"Error: {e}")
        return None


# "Create a {extension} file name {file_name} that calculates factorial of a number"


def read_created_file(command, update_status=None, update_output=None):
    try:
        output_folder = "output"
        # Extract file extension and filename
        words = command.lower().split()
        print(words)
        if "file" in words and "name" in words:
            ext = next((w for w in words if w in ["text", "python", "html", "java", "json", "javascript", "php"]), "text")
            name_index = words.index("name") + 1
            filename = words[name_index]

            extension = {
                "text": ".txt",
                "python": ".py",
                "html": ".html",
                "java": ".java",
                "javascript": ".js",
                "php": ".php",
                "json": ".json"
            }.get(ext, ".txt")

            full_filename = f"{filename}{extension}"
            # Create full path with output folder
            file_path = os.path.join(output_folder, full_filename)

            if not os.path.exists(file_path):
                msg = f"File '{full_filename}' does not exist in output folder."
                if update_output:
                    update_output(msg)
                if update_status:
                    update_status("File not found")
                speak("Sorry, I couldn't find the file.")
                return

            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            if update_status:
                update_status(f"Reading {file_path}")
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