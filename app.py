import streamlit as st
import requests

# Set page config
st.set_page_config(page_title="AI Code Generator", layout="centered")

# Initialize session state for theme
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

# Toggle switch
dark_mode = st.toggle("🌗 Dark Mode", value=st.session_state.dark_mode)
st.session_state.dark_mode = dark_mode

# CSS for dark and light mode
dark_css = """
    <style>
        body, .main {
            background-color: #121212 !important;
            color: #f1f1f1 !important;
        }
        .stTextInput, .stTextArea, .stSelectbox, .stButton > button {
            background-color: #1e1e1e !important;
            color: white !important;
            border: 1px solid #333;
        }
        .stButton > button {
            background-color: #0d6efd;
        }
        .stButton > button:hover {
            background-color: #0b5ed7;
        }
    </style>
"""

light_css = """
    <style>
        body, .main {
            background-color: #f0f2f6 !important;
            color: #000 !important;
        }
        .stTextInput, .stTextArea, .stSelectbox, .stButton > button {
            background-color: white !important;
            color: black !important;
        }
        .stButton > button {
            background-color: #007acc;
            color: white;
        }
        .stButton > button:hover {
            background-color: #005f99;
        }
    </style>
"""

# Apply appropriate theme
st.markdown(dark_css if dark_mode else light_css, unsafe_allow_html=True)

# Container styling
st.markdown("<div class='main'>", unsafe_allow_html=True)
st.markdown("### 💻 AI Code Generator")
st.markdown("### 🧠 Describe what you want and pick your language:")

# Language selection
languages = {
    "Python": "py", "JavaScript": "js", "Java": "java",
    "C++": "cpp", "C": "c", "C#": "cs", "HTML": "html",
    "CSS": "css", "TypeScript": "ts", "Go": "go",
    "Ruby": "rb", "PHP": "php"
}
language_name = st.selectbox("Select a programming language:", list(languages.keys()))
language_code = languages[language_name]

# User input
user_prompt = st.text_area("Enter your code request:", placeholder=f"e.g. Create a login page using {language_name}")

# OpenRouter API setup
OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]
OPENROUTER_ENDPOINT = "https://openrouter.ai/api/v1/chat/completions"

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

# Generate code
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
                mime="text/plain"
            )
    else:
        st.warning("Please enter a description for the code.")

st.markdown("</div>", unsafe_allow_html=True)
