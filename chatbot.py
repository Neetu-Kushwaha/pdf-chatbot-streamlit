import streamlit as st
import os
import fitz  # PyMuPDF
import io
from pdf_extraction import main, chat_openai  # Import the specific function
import time


# Initialize session state to store chat messages and track conversation
if "messages" not in st.session_state:
    st.session_state.messages = []
if "conversation_started" not in st.session_state:
    st.session_state.conversation_started = False
if "conversation_ended" not in st.session_state:
    st.session_state.conversation_ended = False
if "follow_up_asked" not in st.session_state:
    st.session_state.follow_up_asked = False
if "pdf_document" not in st.session_state:
    st.session_state.pdf_document = None
if "new_texts" not in st.session_state:
    st.session_state.new_texts = None  # Store new texts extracted from PDF


# Function to handle the PDF upload, save it, and display success message
def handle_pdf_upload():
    uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

    if uploaded_file is not None:
        # Save the uploaded PDF to the current working directory
        file_path = os.path.join(os.getcwd(), uploaded_file.name)  # Get current directory and save the file

        # Write the uploaded file to the local file system
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Create a delay (simulate processing time)
        st.write("Processing your file... Please wait.")
        time.sleep(4)  # Delay for 2 seconds to simulate processing

        # Display success message with file name
        # st.success(f"PDF file '{uploaded_file.name}' uploaded successfully and saved to {file_path}!")
        st.success(f"PDF file '{uploaded_file.name}' uploaded successfully and saved.")

        # Pass the saved file path to the main function from main.py
        new_texts = main(file_path)
        st.session_state.new_texts = new_texts  # Store the extracted texts
        st.session_state.pdf_uploaded = True  # Flag to indicate that the PDF is uploaded

# Function to provide bot follow-up questions
def get_follow_up_question():
    questions = [
        "Is there anything specific you're looking for information about?",
        "Would you like details on any particular services or products?",
        "How may I assist you with your current query?",
        "Do you need help with any other topic?",
    ]
    return questions[len(st.session_state.messages) % len(questions)]

# Function to check for stop words in the user input
def check_for_stop_words(user_input):
    stop_words = ["stop", "end", "exit", "thank you"]
    if any(word in user_input.lower() for word in stop_words):
        st.session_state.conversation_ended = True
        st.session_state.messages.append("Bot: Thank you for chatting! Have a great day!")
        reset_conversation()  # Reset the session after ending the conversation
        return True
    return False


# Reset the conversation state to allow a new chat session
def reset_conversation():
    st.session_state.messages = []
    st.session_state.conversation_ended = False
    st.session_state.follow_up_asked = False
    st.session_state.user_input = ""  # Clear any input field value


# Process user input and generate bot's response
def process_user_input():
    user_question = st.session_state.user_input
    if user_question:
        # Append the user's question to the message history
        st.session_state.messages.append(f"User: {user_question}")

        # Check for stop words in user input before responding
        if check_for_stop_words(user_question):
            return

        # Call the chat_openai function to generate the bot's response, passing new_texts
        if st.session_state.new_texts:
            bot_response = chat_openai(user_question, st.session_state.new_texts)
        else:
            bot_response = "I need some text to respond. Please upload a PDF."
        time.sleep(4)  # Delay for 2 seconds to simulate processing
        # Append bot's response to the message history
        st.session_state.messages.append(f"Bot: {bot_response}")

        # Ask a follow-up question if necessary
        if len(st.session_state.messages) % 2 != 0:
            follow_up_question = get_follow_up_question()
            st.session_state.messages.append(f"Bot: {follow_up_question}")
            st.session_state.follow_up_asked = True  # Mark that follow-up has been asked

        # Clear the user input field for the next question
        st.session_state.user_input = ""


# Main chat interface with improved styling
def chatbot_interface():
    # Apply custom CSS for a colorful, attractive chat layout
    st.markdown(
        """
        <style>
            .chat-title {
                font-size: 32px;
                color: #ffffff;
                background-color: #4a4e69;
                padding: 15px;
                border-radius: 10px;
                text-align: center;
                font-weight: bold;
            }
            .user-bubble {
                background-color: #6d597a;
                color: #ffffff;
                padding: 12px;
                border-radius: 20px;
                max-width: 60%;
                margin: 10px auto 10px 0;
                font-size: 16px;
                text-align: right;
            }
            .bot-bubble {
                background-color: #f2e9e4;
                color: #333333;
                padding: 12px;
                border-radius: 20px;
                max-width: 60%;
                margin: 10px 0 10px auto;
                font-size: 16px;
                text-align: left;
            }
            .input-box {
                width: 100%;
                padding: 10px;
                font-size: 18px;
                border: 2px solid #4a4e69;
                border-radius: 5px;
            }
            .input-container {
                text-align: center;
                margin-top: 20px;
            }
            body {
                background-color: #f0f0f5;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<div class="chat-title">Customer Support Chatbot</div>', unsafe_allow_html=True)

    # Display the initial greeting or prompt if conversation is not ended
    if not st.session_state.conversation_ended and st.session_state.conversation_started:
        st.write("Feel free to ask your questions!")

    # Display the chat history
    for i, msg in enumerate(st.session_state.messages):
        if i % 2 == 0:
            # User's message bubble
            st.markdown(
                f'<div class="user-bubble">{msg}</div>',
                unsafe_allow_html=True,
            )
        else:
            # Bot's message bubble
            st.markdown(
                f'<div class="bot-bubble">{msg}</div>',
                unsafe_allow_html=True,
            )

    # If the conversation has ended, show a final thank you message
    if st.session_state.conversation_ended:
        st.markdown(
            '<div class="bot-bubble">Thank you for chatting! Feel free to come back if you have more questions.</div>',
            unsafe_allow_html=True)
        return  # Stop further execution after the conversation ends

    # Handle user input
    user_input = st.text_input("Ask a question:", key="user_input", on_change=process_user_input)


# # Run the chat interface
handle_pdf_upload()  # Upload PDF first
chatbot_interface()  # Start the chatbot

