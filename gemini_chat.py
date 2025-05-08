import os
import re
from dotenv import load_dotenv
import google.generativeai as genai

# Load .env variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Configure Gemini
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.0-flash")

def clean_text(text):
    # Remove markdown symbols
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)  # Bold
    text = re.sub(r'\*(.*?)\*', r'\1', text)      # Italic
    text = re.sub(r'`(.*?)`', r'\1', text)        # Inline code
    text = re.sub(r'^#+\s', '', text, flags=re.MULTILINE)  # Headers
    text = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', text)  # Links
    return text.strip()

def ask_gemini(prompt):
    try:
        response = model.generate_content(prompt)
        return clean_text(response.text)
    except Exception as e:
        return f"Error: {e}"
