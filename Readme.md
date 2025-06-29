💻 Virtual Desktop Assistant (A.U.R.A)

A.U.R.A (Autonomous User Response Assistant) is a Python-based voice-controlled virtual desktop assistant powered by speech recognition and Gemini AI. It performs various system-level tasks and answers queries in real time with intelligent conversational capabilities.

---

🚀 Features

- 🎙️ **Voice Command Integration**  
  Interact hands-free using natural language. Open apps, search the web, set reminders, and more.

- 📄 **Document Summarization**  
  Read and summarize PDF and Word documents of any size using Gemini AI. Handles large documents by chunking them intelligently.

- 🤖 **Gemini AI Integration**  
  Leverages Google's Gemini API to answer complex queries, summarize content, generate ideas, and provide contextual suggestions.

- 🗂️ **Task Automation**  
  Automates daily tasks like opening files, checking the weather, and managing reminders.

- 🧠 **Smart Context Handling**  
  Understands context for follow-up questions to maintain intelligent conversation flow.

- 🖥️ **GUI Interface** *(Optional)*  
  Animated GUI built using PyQt5/HTML+CSS for smoother interaction.

---

🛠️ Tech Stack

| Technology        | Purpose                             |
|-------------------|-------------------------------------|
| Python            | Core logic                          |
| Pyttsx3           | Text-to-speech                      |
| SpeechRecognition | Voice input                         |
| PyAudio           | Microphone access                   |
| PyQt5 / HTML+CSS  | GUI (optional)                      |
| Gemini API        | Conversational AI & Document Summarization |
| PyPDF2            | PDF document processing             |
| python-docx       | Word document processing            |
| MySQL             | Persistent storage (e.g. reminders) |

📦 Installation

1. **Clone the repository:**

```bash
git clone https://github.com/sanket-sakariya/A.U.R.A.git
cd virtual-desktop-assistant
```

2. **Install dependencies:**

```bash
pip install -r requirements.txt
```

3. **Set up your API key for Gemini (if required):**

Create a `.env` file:

```bash
GEMINI_API_KEY=your_api_key_here
```

4. **Run the assistant:**

```bash
python run.py
```

---

## 📄 Document Summarization

The assistant can now read and summarize PDF and Word documents of any size:

### Features:
- **Multi-format Support**: PDF (.pdf), Word (.docx, .doc)
- **Large Document Handling**: Automatically chunks large documents for processing
- **Intelligent Summarization**: Uses Gemini AI for comprehensive summaries
- **Progress Tracking**: Shows processing status and file information

### Usage Commands:
- `"summarize document.pdf"` - Summarize a PDF file
- `"summary of report.docx"` - Summarize a Word document
- `"read and summarize presentation.pdf"` - Alternative command format
- `"summarize the file report.docx"` - Another command variation

### Example:
```
You: summarize annual_report.pdf
Assistant: Starting to summarize annual_report.pdf...
[Processing document...]
[Creating summary...]
Summary of annual_report.pdf:

This document contains the annual financial report for 2024...
[Detailed summary continues]
```

### Test the Feature:
```bash
# Test with sample documents
python test_document_summary.py

# Or use the assistant directly
python run.py
# Then say: "summarize filename.pdf"
```

## 🧠 Sample Commands

* "Open Google Chrome"
* "What's the weather today?"
* "Tell me a joke"
* "Play Hanuman Chalisha on youtube"
* "Search from the wikipedia"
* "Create file and write content"
* "Summarize document.pdf"
* "Summary of report.docx"
* "Brighness, Volume, Lock, etc computer commands"


## ✅ To-Do

* [ ] Add more system commands
* [ ] Support offline mode
* [ ] Add personalized greetings
* [ ] Improve GUI animations
* [ ] Add support for more document formats (Excel, PowerPoint)

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---


## 🙋‍♂️ Author

**Sanket Sakariya**
📧 \[sanketsakariya2005@gmail.com]
🌐 \[https://sanket-sakariya.netlify.app/]

---

```

Let me know if you'd like me to add your actual email, GitHub, or a sample license file.
```
