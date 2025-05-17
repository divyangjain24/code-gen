import streamlit as st
import requests
import base64

# Load API Key
OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]
OPENROUTER_ENDPOINT = "https://openrouter.ai/api/v1/chat/completions"

# Page Configuration
st.set_page_config(page_title="AI Code Generator", layout="centered")

# Dark Mode Toggle
dark_mode = st.toggle("🌗 Toggle Dark Mode", value=True)

# Custom CSS with Gradient and Toggle Support
st.markdown(f"""
    <style>
        body {{
            background: linear-gradient(to right, #0f2027, #203a43, #2c5364) if {dark_mode} else #f0f2f6;
        }}
        .main {{
            background: rgba(255, 255, 255, 0.07);
            backdrop-filter: blur(10px);
            padding: 2.5rem;
            border-radius: 15px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.2);
            max-width: 800px;
            margin: auto;
            color: {'white' if dark_mode else '#000'};
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
        .export-button {{
            text-align: right;
            margin-top: 10px;
        }}
    </style>
""", unsafe_allow_html=True)

# Title and instructions
st.markdown("<div class='main'><h1>💻 AI Code Generator</h1>", unsafe_allow_html=True)
st.markdown("### 🧠 Describe what you want and pick your language:")

# Language selector
languages = {
    "Python": "python", "JavaScript": "javascript", "Java": "java",
    "C++": "cpp", "C": "c", "C#": "csharp", "HTML": "html",
    "CSS": "css", "TypeScript": "typescript", "Go": "go",
    "Ruby": "ruby", "PHP": "php"
}
language_name = st.selectbox("Select a programming language:", list(languages.keys()))
language_code = languages[language_name]

# User input prompt
user_prompt = st.text_area("Enter your code request:", placeholder=f"e.g. Create a login page using {language_name}")

# Call OpenRouter API
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
    except Exception as e:
        return f"❌ Error: {str(e)}"

# Generate button and display output
if st.button("✨ Generate Code"):
    if user_prompt.strip():
        with st.spinner("Generating your code..."):
            code_output = generate_code(user_prompt, language_name)
            st.markdown(f"### 🚀 Code Output in {language_name}:")
            st.code(code_output, language=language_code)

            # Download Code Option
            b64 = base64.b64encode(code_output.encode()).decode()
            href = f'<a href="data:file/text;base64,{b64}" download="generated_code.{language_code}">📥 Download Code</a>'
            st.markdown(f"<div class='export-button'>{href}</div>", unsafe_allow_html=True)
    else:
        st.warning("Please enter a description for the code.")

st.markdown("</div>", unsafe_allow_html=True)
