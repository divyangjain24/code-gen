import streamlit as st
import requests
import base64

# --- CONFIGURATION ---
OPENROUTER_API_KEY = st.secrets.get("OPENROUTER_API_KEY")
OPENROUTER_ENDPOINT = "https://openrouter.ai/api/v1/chat/completions"

if not OPENROUTER_API_KEY:
    st.error("API Key not found. Please set OPENROUTER_API_KEY in your Streamlit secrets.")
    st.stop()

# --- PAGE SETUP ---
st.set_page_config(
    page_title="AI Code Generator",
    page_icon="💡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS STYLING ---
st.markdown(open("style.css").read(), unsafe_allow_html=True)

# --- HEADER ---
st.markdown("""
<div class="app-header">
    <img src="https://img.icons8.com/ios-filled/70/00c9ff/code.png" alt="Logo"/>
    <div class="app-title">AI Code Generator</div>
</div>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown(
        '<img class="sidebar-profile-image" src="https://avatars.githubusercontent.com/u/583231?v=4" alt="Profile Image"/>',
        unsafe_allow_html=True
    )
    st.markdown("""
    <div class="info-section">
        <h2 class="info-title">About the Developer</h2>
        <p class="info-text">Email: Narutouzu@gmail.com</p>
        <p class="info-text">Instagram: <a href="https://www.instagram.com/__morningstar7854/" target="_blank" class="info-link">morningstar7854</a></p>
        <p class="info-text">Phone Number: 8630062115</p>
        <p class="info-text">YouTube Channel: <a href="https://www.youtube.com/@alron-mind" target="_blank" class="info-link">Alron Mind</a></p>
        <p class="info-text">LinkedIn: <a href="https://www.linkedin.com/in/divyang-jain-276032291" target="_blank" class="info-link">Divyang Jain</a></p>
    </div>
    """, unsafe_allow_html=True)

# --- MAIN UI ---
st.markdown('<div class="main-container">', unsafe_allow_html=True)
col1, col2 = st.columns(2)

languages = {
    "Python": "py", "JavaScript": "js", "Java": "java",
    "C++": "cpp", "C": "c", "C#": "cs", "HTML": "html",
    "CSS": "css", "TypeScript": "ts", "Go": "go",
    "Ruby": "rb", "PHP": "php"
}

with col1:
    st.markdown('### 🧠 Describe what you want and pick your language:')
    language_name = st.selectbox("Select a programming language:", list(languages.keys()))
    user_prompt = st.text_area(
        "Enter your code request:",
        placeholder=f"e.g. Create a responsive login page using {language_name}",
        height=180,
        max_chars=1000
    )
    generate_button = st.button("🚀 Generate Code")

with col2:
    st.markdown('### 💻 Generated Code Output:')
    code_output = st.empty()

# --- HELPER FUNCTION ---
def generate_code(prompt, language_code):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": f"You are a code generator. Respond only with valid code in {language_code}."},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(OPENROUTER_ENDPOINT, headers=headers, json=data)
        response.raise_for_status()
        code = response.json()["choices"][0]["message"]["content"]
        return code
    except Exception as e:
        return f"⚠️ Error generating code: {e}"

# --- ACTION ---
if generate_button:
    if not user_prompt.strip():
        st.warning("Please enter a prompt to generate code.")
    else:
        with st.spinner("Generating code..."):
            language_code = languages[language_name]
            output_code = generate_code(user_prompt, language_code)
            code_output.code(output_code, language_code)

st.markdown('</div>', unsafe_allow_html=True)
