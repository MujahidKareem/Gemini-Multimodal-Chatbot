import streamlit as st
import google.generativeai as genai
import datetime
import speech_recognition as sr
import base64
import docx
from PyPDF2 import PdfReader
from PIL import Image
import io

# Set API key
GOOGLE_API_KEY = "AIzaSyDARjXLoKDdgaCOfC6-2Ud6pGa2ZOUu3BE"  # Replace with your Gemini API key
genai.configure(api_key=GOOGLE_API_KEY)

# Create Gemini model instance
model = genai.GenerativeModel("models/gemini-1.5-flash")

# --- Streamlit Page Config ---
st.set_page_config(
    page_title="Gemini Chatbot | Mujahid Kareem",
    page_icon="🤖",
    layout="centered"
)

# --- Custom Styling ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');
   
    .stApp {
        color: #1e293b;
        font-family: 'Roboto', sans-serif;
         background:#34cdeb;
    }
    .chatbox {
        background-color: #1e293b !important;
        padding: 1rem;
        border-radius: 14px;
        margin: 0.5rem 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
        z-index:999;
        
    }
    .block-container{
        background:#348feb;
        padding:0px 50px;
        min-height:80vh;
        border-radius:20px;
        overflow:auto;
    }
    .st-emotion-cache-z4kicb{
            justify-content: center;
    }
    .user-msg {
        color: #60a5fa;
        font-weight: 600;
    }
    .bot-msg {
        color: #34d399;
        font-weight: 600;
    }
    .chat-form-wrapper {
        background-color: red;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 0 20px rgba(0,0,0,0.2);
        color: #1e293b;
        border: 2px solid #475569;
    }
    .footer {
        text-align: center;
        font-size: 0.9rem;
        color: #1e293b;
        padding:20px 0px
    }
    .avatar {
        width: 28px;
        height: 28px;
        border-radius: 50%;
        display: inline-block;
        margin-right: 10px;
        vertical-align: middle;
    }
    .chat-label {
        font-size: 0.95rem;
        font-weight: bold;
        margin-right: 6px;
    }
    .timestamp {
        font-size: 0.75rem;
        color: #94a3b8;
        margin-left: 8px;
    }
    input[type="text"] {
        border: 1px solid #cbd5e1;
        border-radius: 10px;
        padding: 10px;
        font-size: 16px;
        width: 100%;
    }
    .st-emotion-cache-1bcyifm {
    border: 1px solid rgba(49, 51, 63, 0.2);
    border-radius: 0.5rem;
    padding: calc(-1px + 1rem);
    width: 100%;
    height: 100%;
    overflow: visible;
    background-color: #346beb;
}
    </style>
""", unsafe_allow_html=True)

# --- Title ---
st.markdown("""
    <h1 style='text-align: center; color: #1e293b;'>🤖 Gemini Chatbot</h1>
    <p style='text-align: center; color: #334155;'>Modern, professional AI assistant powered by Gemini API</p>
    <hr style='border: 1px solid #475569;'>
""", unsafe_allow_html=True)

# --- Chat Memory ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Chat Display ---
for role, msg, ts in st.session_state.messages:
    role_class = "user-msg" if role == "user" else "bot-msg"
    avatar_url = "https://cdn-icons-png.flaticon.com/512/1077/1077063.png" if role == "user" else "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d9/Google_Gemini_logo.svg/240px-Google_Gemini_logo.svg.png"
    st.markdown(
        f"""
        <div class='chatbox {role_class}'>
            <img class='avatar' src='{avatar_url}' />
            <span class='chat-label'>{'You' if role=='user' else 'Gemini'}</span>
            <span class='timestamp'>{ts}</span><br>{msg}
        </div>
        """, unsafe_allow_html=True)

# --- Voice Input Function ---
def record_voice():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        with st.spinner("🎹 Listening..."):
            audio = recognizer.listen(source, phrase_time_limit=5)
    try:
        text = recognizer.recognize_google(audio)
        return text
    except Exception as e:
        return f"❌ Voice recognition error: {e}"

# --- Input Form ---
with st.form(key="chat_form"):
    user_input = st.text_input("💬 Type your message:", key="input")
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        voice_input = st.form_submit_button("🎤 Speak")
    with col2:
        file_input = st.file_uploader("📌 Upload File", type=None, label_visibility="collapsed")
    with col3:
        submit = st.form_submit_button("📩 Send")

# --- Voice Input Logic ---
if voice_input:
    user_input = record_voice()
    st.session_state.messages.append(("user", user_input, datetime.datetime.now().strftime("%H:%M")))
    try:
        response = model.generate_content(user_input)
        bot_reply = response.text
    except Exception as e:
        bot_reply = "❌ Error: " + str(e)
    st.session_state.messages.append(("bot", bot_reply, datetime.datetime.now().strftime("%H:%M")))
    st.rerun()

# --- File Upload Handling ---
if submit and file_input is not None:
    file_type = file_input.type
    content = ""
    try:
        if "image" in file_type:
            image = Image.open(file_input)
            st.image(image, caption="Uploaded Image", use_container_width=True)
            if image.mode == "RGBA":
                image = image.convert("RGB")
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='JPEG')
            image_bytes = img_byte_arr.getvalue()
            content = [{"inline_data": {"mime_type": "image/jpeg", "data": base64.b64encode(image_bytes).decode()}}]
            response = model.generate_content(contents=[{"parts": content}])
            bot_reply = response.text
            st.session_state.messages.append(("user", "Describe this image.", datetime.datetime.now().strftime("%H:%M")))
            st.session_state.messages.append(("bot", bot_reply, datetime.datetime.now().strftime("%H:%M")))
            st.rerun()
        elif "pdf" in file_type:
            reader = PdfReader(file_input)
            content = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
        elif "word" in file_type or "msword" in file_type or file_input.name.endswith(".docx"):
            doc = docx.Document(file_input)
            content = "\n".join([para.text for para in doc.paragraphs])
        else:
            content = "Unsupported file type."

        if content and not isinstance(content, list):
            st.markdown("**Extracted Content:**")
            st.write(content)
            response = model.generate_content(content)
            st.session_state.messages.append(("user", content, datetime.datetime.now().strftime("%H:%M")))
            st.session_state.messages.append(("bot", response.text, datetime.datetime.now().strftime("%H:%M")))
            st.rerun()
    except Exception as e:
        st.error(f"❌ Failed to analyze file: {e}")

# --- Text Input Submit Logic ---
elif submit and user_input:
    timestamp = datetime.datetime.now().strftime("%H:%M")
    st.session_state.messages.append(("user", user_input, timestamp))
    try:
        response = model.generate_content(user_input)
        bot_reply = response.text
    except Exception as e:
        bot_reply = "❌ Error: " + str(e)
    st.session_state.messages.append(("bot", bot_reply, timestamp))
    st.rerun()

# --- Footer ---
st.markdown("""
    <div class='footer'>
        <hr style='border: 0.5px solid #64748b;'>
        Gemini Chatbot &copy; 2025 — <strong>Designed, Built & Engineered by AI Engineer Mujahid Kareem</strong>
    </div>
""", unsafe_allow_html=True)
