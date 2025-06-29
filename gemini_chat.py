import os
import re
from dotenv import load_dotenv
import google.generativeai as genai  # type: ignore

# Load .env variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Configure Gemini
genai.configure(api_key=api_key)  # type: ignore
model = genai.GenerativeModel('gemini-1.5-flash')  # type: ignore

def clean_text(text):
    # Remove markdown symbols
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)  # Bold
    text = re.sub(r'\*(.*?)\*', r'\1', text)      # Italic
    text = re.sub(r'`(.*?)`', r'\1', text)        # Inline code
    text = re.sub(r'^#+\s', '', text, flags=re.MULTILINE)  # Headers
    text = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', text)  # Links
    return text.strip()

def extract_text_from_pdf(file_path):
    """Extract text from PDF file"""
    try:
        import PyPDF2
        text = ""
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        return text.strip()
    except ImportError:
        return "Error: PyPDF2 library not installed. Please install it using: pip install PyPDF2"
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

def extract_text_from_docx(file_path):
    """Extract text from Word document"""
    try:
        from docx import Document
        doc = Document(file_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text.strip()
    except ImportError:
        return "Error: python-docx library not installed. Please install it using: pip install python-docx"
    except Exception as e:
        return f"Error reading Word document: {str(e)}"

def chunk_text(text, max_chunk_size=30000):
    """Split text into chunks for processing large documents"""
    if len(text) <= max_chunk_size:
        return [text]
    
    chunks = []
    current_chunk = ""
    sentences = text.split('. ')
    
    for sentence in sentences:
        if len(current_chunk + sentence) < max_chunk_size:
            current_chunk += sentence + '. '
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = sentence + '. '
    
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks

def summarize_document_chunk(chunk, document_type="document"):
    """Summarize a single chunk of document text"""
    try:
        prompt = f"""
Please provide a comprehensive summary of the following {document_type} content. 
Focus on the main points, key information, and important details, Give the summary in 100 words.

Content:
{chunk}

Please provide a clear, well-structured summary that captures the essential information.
"""
        response = model.generate_content(prompt)
        return clean_text(response.text)
    except Exception as e:
        return f"Error summarizing chunk: {str(e)}"

def summarize_document(file_path, update_status=None, update_output=None):
    """Read and summarize PDF or Word documents"""
    try:
        if not os.path.exists(file_path):
            return f"Error: File '{file_path}' not found."
        
        file_extension = os.path.splitext(file_path)[1].lower()
        
        if update_status:
            update_status(f"Reading {file_extension.upper()} document...")
        
        # Extract text based on file type
        if file_extension == '.pdf':
            text = extract_text_from_pdf(file_path)
            document_type = "PDF document"
        elif file_extension in ['.docx', '.doc']:
            text = extract_text_from_docx(file_path)
            document_type = "Word document"
        else:
            return f"Error: Unsupported file format '{file_extension}'. Supported formats: PDF (.pdf), Word (.docx, .doc)"
        
        if text.startswith("Error:"):
            return text
        
        if not text.strip():
            return "Error: No text content found in the document."
        
        # Get file size info
        file_size = os.path.getsize(file_path) / (1024 * 1024)  # Size in MB
        text_length = len(text)
        
        if update_output:
            update_output(f"Document size: {file_size:.2f} MB, Text length: {text_length:,} characters")
        
        # Chunk the text if it's too large
        chunks = chunk_text(text)
        
        if len(chunks) == 1:
            # Single chunk - summarize directly
            if update_status:
                update_status("Summarizing document...")
            
            summary = summarize_document_chunk(chunks[0], document_type)
            
            if update_status:
                update_status("Document summarized successfully")
            
            return f"Summary of {os.path.basename(file_path)}:\n\n{summary}"
        
        else:
            # Multiple chunks - summarize each and then create a final summary
            if update_status:
                update_status(f"Processing large document ({len(chunks)} chunks)...")
            
            chunk_summaries = []
            for i, chunk in enumerate(chunks, 1):
                if update_output:
                    update_output(f"Processing chunk {i}/{len(chunks)}...")
                
                chunk_summary = summarize_document_chunk(chunk, document_type)
                chunk_summaries.append(chunk_summary)
            
            # Create final summary from all chunk summaries
            if update_status:
                update_status("Creating final summary...")
            
            final_summary_prompt = f"""
I have a {document_type} that was too large to process at once, so I've summarized it into {len(chunks)} parts. 
Please create a comprehensive final summary that combines all these summaries into one coherent summary.

Summaries:
{chr(10).join(f"Part {i+1}: {summary}" for i, summary in enumerate(chunk_summaries))}

Please provide a well-structured final summary that captures all the important information from the document.
"""
            
            final_summary = model.generate_content(final_summary_prompt)
            final_summary_text = clean_text(final_summary.text)
            
            if update_status:
                update_status("Document summarized successfully")
            
            return f"Summary of {os.path.basename(file_path)}:\n\n{final_summary_text}"
    
    except Exception as e:
        return f"Error processing document: {str(e)}"

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