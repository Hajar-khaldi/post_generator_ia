# 🤖 Generative AI – Social Media Post Generator

This project is a Streamlit web application that generates optimized LinkedIn and Facebook posts from user-provided keywords using a Large Language Model (LLaMA) via the Hugging Face Inference API.

## 🚀 Features
- Keyword-based post generation
- LinkedIn / Facebook style selection
- Token-based length control
- Markdown formatted output
- Editable post preview
- Copy-to-clipboard functionality
- Clean two-column UI layout

## 🧠 Technologies Used
- **LLM**: LLaMA 3.1 (Hugging Face Inference API)
- **Backend**: Python
- **Frontend**: Streamlit
- **NLP**: Hugging Face Transformers (API-based)
- **Version Control**: Git & GitHub

## 🔐 Environment Variable
This project requires a Hugging Face API token.

Set it before running the app:

Linux / macOS
```bash
export HF_TOKEN=your_huggingface_token

Windows (PowerShell)
```bash
setx HF_TOKEN "your_huggingface_token"

Or using Streamlit secrets (.streamlit/secrets.toml):
```bash
HF_TOKEN="your_huggingface_token"
```

## ▶️ Run the Project
**1.Clone the repository:**
```bash
git clone https://github.com/your-username/post_generator_ia.git
cd post_generator_ia
```

**2.Install dependencies:**
```bash
pip install -r requirements.txt
```

**3.Run the Streamlit app:**
```bash
streamlit run app.py
```

**4.Open your browser at:**
```bash
http://localhost:8501
```
