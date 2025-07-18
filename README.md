🤖 Gemini Multimodal Chatbot

A modern, multimodal AI assistant built using "Google Gemini 1.5 Flash API", capable of interacting through "text, voice, image", and "document uploads". Designed with an elegant "Streamlit interface" to simulate real-world use cases for Generative AI.

---

 🌟 Features

- 💬 Text Chat — Real-time chat interface
- 🎤 Voice Input — Convert your speech into queries
- 📄 PDF & Word Upload — Extracts and analyzes content
- 🖼️ Image Upload — Describes and interprets images
- 🧠 Gemini 1.5 Flash API — Fast and capable multimodal model
- 🎨 Beautiful and professional UI with custom CSS

---

🛠️ Tech Stack

| Tech                  | Role                             |
|-----------------------|----------------------------------|
| `Streamlit`           | Frontend / UI Framework          |
| `google.generativeai` | Gemini API integration           |
| `SpeechRecognition`   | Voice-to-text                    |
| `PyPDF2`, `docx`      | PDF and Word document handling   |
| `Pillow` (PIL)        | Image reading and preprocessing  |
| `base64`, `io`        | Encoding and memory handling     |

---
 🚀 Getting Started

 🔧 Install Requirements

```bash
pip install streamlit google-generativeai SpeechRecognition pypdf2 python-docx Pillow
````

 🔑 Set Up Gemini API

Get your Gemini API key from: [Google AI Studio](https://makersuite.google.com/app)

Then set your key:

```python
GOOGLE_API_KEY = "your_api_key_here"
genai.configure(api_key=GOOGLE_API_KEY)
```

 ▶️ Run the App

```bash
streamlit run app.py
```

---

 📁 Supported File Types

 `.pdf` – Extracts full text
 `.docx` – Extracts paragraphs
 `.jpg`, `.jpeg`, `.png` – Gemini interprets visual content

---

 🙋‍♂️ Author

Mujahid Kareem
🎓 AI Engineer | Generative AI Enthusiast
🌍 Based in Pakistan | Open to collaboration and freelance projects

---

## 🌐 Connect with Me

* 🔗 [LinkedIn](https://www.linkedin.com/in/mujahid-kareem-9aa68b308?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app)
* 🧠 [GitHub](https://github.com/MujahidKareem)
* 📬 Email: [mujahidkareem1122@gmail.com)

---

## 📃 License

This project is open-source under the [MIT License](LICENSE).

---

> “AI will not replace you. A person using AI will.”
> — Stay ahead by building intelligent tools today.
