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
        # Define custom responses for basic chat questions
        basic_responses = {
            "who developed you": "I am developed by Sanket Sakariya and team.",
            "who created you": "I am created by Sanket Sakariya and team.",
            "who made you": "I am made by Sanket Sakariya and team.",
            "who built you": "I am built by Sanket Sakariya and team.",
            "who are you": "I am A.U.R.A. an AI assistant developed by Sanket Sakariya and team.",
            "what are you": "I am A.U.R.A. an AI assistant created by Sanket Sakariya and team.",
            "your developer": "My developer is Sanket Sakariya and team.",
            "your creator": "My creator is Sanket Sakariya and team.",
            "who is your developer": "My developer is Sanket Sakariya and team.",
            "who is your creator": "My creator is Sanket Sakariya and team.",
            "what is your name": "I am A.U.R.A. an AI assistant developed by Sanket Sakariya and team.",
            "your name": "A.U.R.A.",
            "introduce yourself": "Hello! I am A.U.R.A. an AI assistant developed by Sanket Sakariya and team. I'm here to help you with your questions and tasks.",
            "about you": "I am A.U.R.A. an AI assistant created by Sanket Sakariya and team to help users with various questions and tasks.",
            "tell me about yourself": "I am an AI assistant developed by Sanket Sakariya and team. I'm designed to be helpful, informative, and assist you with various queries."
        }
        
        # Check if the prompt matches any basic chat question
        prompt_lower = prompt.lower().strip()
        for key, response in basic_responses.items():
            if key in prompt_lower:
                return response
        
        # Continue with normal processing for other questions
        is_deep_search = "deep search" in prompt.lower()
        clean_prompt = prompt.replace("deep search", "").strip()

        if not is_deep_search:
            # Add instruction to keep the answer brief
            clean_prompt += "\nPlease keep the answer short and concise (within 50-100 words). or if answer is possible in a single line."

        response = model.generate_content(clean_prompt)
        return clean_text(response.text)
    except Exception as e:
        return f"Error: {e}"
