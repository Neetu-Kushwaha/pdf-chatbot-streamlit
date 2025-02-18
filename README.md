# RAG-based PDF Chatbot with Streamlit

## Overview
This project is a **Retrieval-Augmented Generation (RAG) chatbot** built using **Streamlit** that allows users to upload a PDF file and interact with an AI chatbot that extracts and retrieves relevant information from the document. The chatbot leverages OpenAI's language model to generate responses based on extracted text.

## Features
- **Upload and process PDF files**
- **Extract and retrieve relevant text from PDFs** using `PyMuPDF (fitz)`
- **Conversational chatbot** using `OpenAI API`
- **Custom chatbot interface** with enhanced styling
- **Session management** to track conversation history

## Installation
To set up and run this chatbot locally, follow these steps:

### 1. Clone the repository
```bash
git clone https://github.com/your-username/pdf-chatbot-streamlit.git
cd pdf-chatbot-streamlit
```

### 2. Install dependencies
Make sure you have Python installed, then install the required libraries:
```bash
pip install -r requirements.txt
```

### 3. Run the chatbot
```bash
streamlit run main.py
```

## Dependencies
This project uses the following libraries:
- `streamlit` for UI
- `PyMuPDF (fitz)` for PDF processing
- `openai` for chatbot interaction
- `os`, `io`, `time` for file handling and delays

## Usage
1. Upload a PDF file.
2. Wait for the file to process.
3. Start chatting with the bot.
4. The bot retrieves relevant sections from the PDF and generates responses.
5. Type "stop", "end", or "exit" to terminate the conversation.

## Folder Structure
```
/pdf-chatbot-streamlit
│── QA_without_runnable.py  #  QA-RAG module using langchain and openai
│── chatbot.py              # Chatbot logic
│── multi_column.py         # Utility for handling multi-column text
│── main.py                 # Main Streamlit app
│── pdf_extraction.py       # PDF processing and retrieval functions
│── requirements.txt        # Dependencies
│── README.md               # Project documentation
```

## Future Enhancements
- **Multi-PDF support**
- **Advanced retrieval techniques for better accuracy**
- **Database integration for storing chat history**
- **Deployment on cloud services**

## License
This project is licensed under the MIT License.


