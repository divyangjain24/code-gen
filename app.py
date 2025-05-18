import streamlit as st
import requests
import base64

# Config
OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]
OPENROUTER_ENDPOINT = "https://openrouter.ai/api/v1/chat/completions"

# Page Setup
st.set_page_config(
    page_title="AI Code Generator",
    page_icon="💡",
    layout="centered"
)

# Custom Styles
st.markdown("""
    <style>
        html, body, .stApp {
            background-color: #0e1117 !important;
            color: white !important;
            font-family: 'Segoe UI', sans-serif;
        }
        textarea, input, select {
            background-color: #1e1e2f !important;
            color: white !important;
            border-radius: 8px !important;
        }
        .stButton > button {
            background-color: #00c9ff !important;
            color: black !important;
            font-weight: bold;
            border-radius: 8px;
            transition: background-color 0.3s ease;
        }
        .stButton > button:hover {
            background-color: #009ec3 !important;
        }
        .app-header {
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 20px 0;
            margin-bottom: 25px;
        }
        .app-title {
            font-size: 32px;
            font-weight: 700;
            color: #00c9ff;
        }
        .export-button {
            text-align: right;
            margin-top: 10px;
        }
        .info-section {
            margin-top: 60px;
            border-top: 1px solid #333;
            padding-top: 20px;
            font-size: 16px;
        }
        .info-title {
            color: #f56565;
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .info-text, .info-link {
            color: #cbd5e0;
        }
        .info-link:hover {
            color: #63b3ed;
        }
    </style>
""", unsafe_allow_html=True)

# Logo + Title
st.markdown("""
    <div class="app-header">
        <img src="https://img.icons8.com/external-wanicon-lineal-color-wanicon/96/000000/artificial-intelligence.png" width="80">
        <div class="app-title">AI Code Generator</div>
    </div>
""", unsafe_allow_html=True)

# Input UI
st.markdown("### 🧠 Describe what you want and pick your language:")

languages = {
    "Python": "py", "JavaScript": "js", "Java": "java",
    "C++": "cpp", "C": "c", "C#": "cs", "HTML": "html",
    "CSS": "css", "TypeScript": "ts", "Go": "go",
    "Ruby": "rb", "PHP": "php"
}

language_name = st.selectbox("Select a programming language:", list(languages.keys()))
language_code = languages[language_name]

user_prompt = st.text_area("Enter your code request:", placeholder=f"e.g. Create a login page using {language_name}")

# Generate Code Function
def generate_code(prompt, lang):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": f"You are a professional {lang} developer."},
            {"role": "user", "content": f"Generate an optimal and correct {lang} solution for:\n{prompt}\nOnly provide the code."}
        ],
        "temperature": 0.5,
        "max_tokens": 1000
    }

    try:
        response = requests.post(OPENROUTER_ENDPOINT, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        return f"❌ Error: {str(e)}. Please check your network connection and OpenRouter API key."
    except KeyError:
        return "❌ Error: Could not extract code from the API response. The API may have returned an unexpected format."
    except Exception as e:
        return f"❌ Error: An unexpected error occurred: {str(e)}"

# Generate Button
if st.button("✨ Generate Code"):
    if user_prompt.strip():
        with st.spinner("Generating your code..."):
            code_output = generate_code(user_prompt, language_name)
            st.markdown(f"### 🚀 Code Output in {language_name}:")
            st.code(code_output, language=language_code)

            # Download button
            b64 = base64.b64encode(code_output.encode()).decode()
            href = f'<a href="data:file/text;base64,{b64}" download="generated_code.{language_code}">📥 Download Code</a>'
            st.markdown(f"<div class='export-button'>{href}</div>", unsafe_allow_html=True)
    else:
        st.warning("⚠️ Please enter a code request before generating.")

# Developer Info
st.markdown("""
<div class="info-section">
    <div class="info-title">About the Developer</div>
    <p class="info-text">Email: <a href="mailto:Narutouzu@gmail.com" class="info-link">Narutouzu@gmail.com</a></p>
    <p class="info-text">Instagram: <a href="https://www.instagram.com/__morningstar7854/" target="_blank" class="info-link">morningstar7854</a></p>
    <p class="info-text">Phone: 8630062115</p>
    <p class="info-text">YouTube: <a href="https://www.youtube.com/@alron-mind" target="_blank" class="info-link">Alron Mind</a></p>
    <p class="info-text">LinkedIn: <a href="https://www.linkedin.com/in/divyang-jain-276032291" target="_blank" class="info-link">Divyang Jain</a></p>
</div>
""", unsafe_allow_html=True)
