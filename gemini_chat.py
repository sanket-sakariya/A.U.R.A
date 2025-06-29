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
            "who are you": "I am an AI assistant developed by Sanket Sakariya and team.",
            "what are you": "I am an AI assistant created by Sanket Sakariya and team.",
            "your developer": "My developer is Sanket Sakariya and team.",
            "your creator": "My creator is Sanket Sakariya and team.",
            "who is your developer": "My developer is Sanket Sakariya and team.",
            "who is your creator": "My creator is Sanket Sakariya and team.",
            "what is your name": "I am an AI assistant developed by Sanket Sakariya and team.",
            "your name": "I am an AI assistant created by Sanket Sakariya and team.",
            "introduce yourself": "Hello! I am an AI assistant developed by Sanket Sakariya and team. I'm here to help you with your questions and tasks.",
            "about you": "I am an AI assistant created by Sanket Sakariya and team to help users with various questions and tasks.",
            "tell me about yourself": "I am an AI assistant developed by Sanket Sakariya and team. I'm designed to be helpful, informative, and assist you with various queries."
        }
        
        # Define allowed question categories/keywords
        allowed_categories = [
            # Educational & Learning
            "what is", "how to", "explain", "define", "meaning", "learn", "study", "tutorial", "guide",
            "help me", "teach me", "show me", "example", "difference between", "comparison",
            
            # Technology & Programming
            "python", "programming", "code", "coding", "software", "computer", "technology", "algorithm",
            "debug", "error", "bug", "development", "web", "app", "application", "database",
            
            # General Knowledge
            "history", "science", "math", "mathematics", "physics", "chemistry", "biology", "geography",
            "literature", "art", "music", "culture", "religion", "philosophy", "psychology",
            
            # Practical Help
            "recipe", "cooking", "health", "fitness", "exercise", "diet", "nutrition", "medical",
            "travel", "business", "finance", "money", "investment", "career", "job", "interview",
            
            # Creative & Writing
            "write", "story", "poem", "essay", "letter", "email", "creative", "ideas", "brainstorm",
            "suggest", "recommend", "advice", "tips", "improvement",
            
            # Problem Solving
            "solve", "solution", "problem", "issue", "fix", "repair", "troubleshoot", "calculate",
            "formula", "equation", "analysis", "research", "summary", "review",
            
            # Language & Communication
            "translate", "language", "grammar", "spelling", "pronunciation", "synonym", "antonym",
            "sentence", "paragraph", "communication", "speaking", "writing",
            
            # Current Events & Information
            "news", "current", "latest", "update", "information", "facts", "data", "statistics",
            "report", "analysis", "trend", "development",
            
            # Hobbies & Interests
            "hobby", "game", "sport", "movie", "book", "music", "entertainment", "fun", "activity",
            "craft", "diy", "project", "creative project"
        ]
        
        # coding related keywords
        coding_keywords = [
            "code", "programming", "python", "javascript", "java","c", "c++", "c#", "ruby", "php",
            "html", "css", "sql", "database", "algorithm", "data structure", "debugging",
            "software development", "web development", "app development"
        ]

        # Check if the prompt matches any basic chat question first
        prompt_lower = prompt.lower().strip()
        for key, response in basic_responses.items():
            if key in prompt_lower:
                return response
        
        # Check if the query contains allowed keywords/categories
        is_allowed = any(keyword in prompt_lower for keyword in allowed_categories)
        
        # Additional check for question patterns
        question_patterns = [
            prompt_lower.startswith(("what", "how", "why", "when", "where", "who", "which", "can you", "could you", "would you")),
            "?" in prompt,
            any(word in prompt_lower for word in ["help", "explain", "tell me", "show me", "teach me"])
        ]
        
        has_question_pattern = any(question_patterns)
        
        # Check if the prompt contains coding-related keywords
        is_coding_related = any(keyword in prompt_lower for keyword in coding_keywords)
        if is_coding_related:
            # If coding-related, use code generation
            return code_gemini(prompt)  # Default to Python code generation

        # If not allowed or doesn't match question patterns, return default response
        if not is_allowed and not has_question_pattern:
            return "I don't understand."
        
        # Continue with normal processing for allowed questions
        is_deep_search = "deep search" in prompt.lower()
        clean_prompt = prompt.replace("deep search", "").strip()

        if not is_deep_search:
            # Add instruction to keep the answer brief
            clean_prompt += "\nPlease keep the answer short and concise (within 50-100 words). or if answer is possible in a single line."

        response = model.generate_content(clean_prompt)
        return clean_text(response.text)
        
    except Exception as e:
        return f"Error: {e}"


def code_gemini(prompt,extension=None):
    try:
        clean_prompt = f"""
{prompt}

CRITICAL REQUIREMENTS:
- Generate ONLY {extension} code
- NO comments whatsoever
- NO explanations
- NO markdown code blocks
- NO backticks (`)
- NO language identifiers
- NO text outside the actual code
- Output raw {extension} code ONLY - start directly with code
- Return pure executable {extension} code with no formatting
"""
        
        response = model.generate_content(clean_prompt)
        return clean_text(response.text)
        
    except Exception as e:
        return f"Error: {e}"