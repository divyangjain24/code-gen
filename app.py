import streamlit as st
import requests

# Load API Key
OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]
OPENROUTER_ENDPOINT = "https://openrouter.ai/api/v1/chat/completions"

st.set_page_config(page_title="AI Code Generator", layout="centered")

# Initialize dark mode state
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True

# Dark mode toggle checkbox
dark_mode = st.checkbox("🌗 Toggle Dark Mode", value=st.session_state.dark_mode)
st.session_state.dark_mode = dark_mode

# CSS for dark and light modes
if st.session_state.dark_mode:
    bg_style = """
    body {
        background: linear-gradient(to right, #0f2027, #203a43, #2c5364);
        color: white;
    }
    .main {
        background: rgba(255, 255, 255, 0.07);
        backdrop-filter: blur(10px);
        padding: 2.5rem;
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.2);
        max-width: 800px;
        margin: auto;
        color: white;
    }
    h1 {
        color: #00ffff;
        font-family: 'Courier New', monospace;
        text-align: center;
    }
    .stButton > button {
        background-color: #00c9ff;
        color: black;
        padding: 0.6rem 1.3rem;
        border: none;
        font-weight: bold;
        border-radius: 10px;
    }
    .stButton > button:hover {
        background-color: #009ec3;
        transform: scale(1.04);
    }
    """
else:
    bg_style = """
    body {
        background: #f0f2f6;
        color: black;
    }
    .main {
        background: white;
        padding: 2.5rem;
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        max-width: 800px;
        margin: auto;
        color: black;
    }
    h1 {
        color: #007acc;
        font-family: 'Courier New', monospace;
        text-align: center;
    }
    .stButton > button {
        background-color: #007acc;
        color: white;
        padding: 0.6rem 1.3rem;
        border: none;
        font-weight: bold;
        border-radius: 10px;
    }
    .stButton > button:hover {
        background-color: #005f99;
        transform: scale(1.04);
    }
    """

st.markdown(f"<style>{bg_style}</style>", unsafe_allow_html=True)

st.markdown("<div class='main'>", unsafe_allow_html=True)
st.markdown("### 💻 AI Code Generator")
st.markdown("### 🧠 Describe what you want and pick your language:")

languages = {
    "Python": "py",
    "JavaScript": "js",
    "Java": "java",
    "C++": "cpp",
    "C": "c",
    "C#": "cs",
    "HTML": "html",
    "CSS": "css",
    "TypeScript": "ts",
    "Go": "go",
    "Ruby": "rb",
    "PHP": "php"
}

language_name = st.selectbox("Select a programming language:", list(languages.keys()))
language_code = languages[language_name]

user_prompt = st.text_area("Enter your code request:", placeholder=f"e.g. Create a login page using {language_name}")

def generate_code(prompt, lang):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": f"You are a professional {lang} developer who writes clean, efficient, and well-commented code."},
            {"role": "user", "content": f"Generate an optimal and correct {lang} solution for:\n{prompt}\nOnly provide the code without explanations."}
        ],
        "temperature": 0.5,
        "max_tokens": 1000
    }
    try:
        response = requests.post(OPENROUTER_ENDPOINT, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        if "choices" in result and len(result["choices"]) > 0:
            return result["choices"][0]["message"]["content"]
        else:
            return "⚠️ No code returned from the model."
    except Exception as e:
        return f"❌ Error: {str(e)}"

if st.button("✨ Generate Code"):
    if user_prompt.strip():
        with st.spinner("Generating your code..."):
            code_output = generate_code(user_prompt, language_name)
            st.markdown(f"### 🚀 Code Output in {language_name}:")
            st.code(code_output, language=language_code)

            st.download_button(
                label="📥 Download Code",
                data=code_output,
                file_name=f"generated_code.{language_code}",
                mime="text/plain",
                key="download-code-btn"
            )
    else:
        st.warning("Please enter a description for the code.")

st.markdown("</div>", unsafe_allow_html=True)
