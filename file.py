import os
from gemini_chat import ask_gemini

def create_and_write_file(command, update_status=None, update_output=None):
    try:
        # Extract filename and extension
        words = command.lower().split()
        if "file" in words and "named" in words:
            ext = next((w for w in words if w in ["text", "python", "html", "java", "json"]), "text")
            name_index = words.index("named") + 1
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


# "Create a {extension} file named {file_name} that calculates factorial of a number"