import streamlit as st
import requests

# Load API Key
OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]
OPENROUTER_ENDPOINT = "https://openrouter.ai/api/v1/chat/completions"

st.set_page_config(page_title="AI Code Generator", layout="centered")

# Initialize dark mode state in session_state
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True

def toggle_mode():
    st.session_state.dark_mode = not st.session_state.dark_mode

# Dark Mode Toggle Button
st.button("🌗 Toggle Dark Mode", on_click=toggle_mode)

# Apply CSS based on dark_mode state
if st.session_state.dark_mode:
    background_style = "linear-gradient(to right, #0f2027, #203a43, #2c5364); color: white;"
else:
    background_style = "#f0f2f6; color: black;"

st.markdown(f"""
    <style>
        body {{
            background: {background_style}
        }}
        .main {{
            background: rgba(255, 255, 255, 0.07);
            backdrop-filter: blur(10px);
            padding: 2.5rem;
            border-radius: 15px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.2);
            max-width: 800px;
            margin: auto;
            color: inherit;
        }}
        h1 {{
            text-align: center;
            color: #00ffff;
            font-family: 'Courier New', monospace;
        }}
        .stTextArea, .stSelectbox, .stButton > button {{
            font-size: 1rem;
            border-radius: 10px;
        }}
        .stButton > button {{
            background-color: #00c9ff;
            color: black;
            padding: 0.6rem 1.3rem;
            border: none;
            font-weight: bold;
        }}
        .stButton > button:hover {{
            background-color: #009ec3;
            transform: scale(1.04);
        }}
    </style>
""", unsafe_allow_html=True)

# Title and instructions
st.markdown("<div class='main'><h1>💻 AI Code Generator</h1>", unsafe_allow_html=True)
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
            {"role": "user", "content": f"Generate an optimal and correct {lang} solution for:\n{prompt}\nOnly provide the code without any explanations."}
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
