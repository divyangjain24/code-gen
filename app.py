import streamlit as st
import requests
import base64

# Load API Key from Streamlit secrets
OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]
OPENROUTER_ENDPOINT = "https://openrouter.ai/api/v1/chat/completions"

# Page Configuration
st.set_page_config(page_title="AI Code Generator", layout="centered")

# Apply only dark mode CSS
st.markdown("""
    <style>
        html, body, .stApp {
            background-color: #0e1117 !important;
            color: white !important;
        }
        label, div, p, h1, h2, h3, h4, h5, h6 {
            color: white !important;
        }
        textarea, input, select {
            background-color: #262730 !important;
            color: white !important;
        }
        .stButton > button {
            background-color: #00c9ff !important;
            color: black !important;
            font-weight: bold;
        }
        .stButton > button:hover {
            background-color: #009ec3 !important;
        }

        /* Selectbox & Dropdown Fix */
        div[data-baseweb="select"] {
            background-color: #262730 !important;
            color: white !important;
        }
        div[data-baseweb="select"] * {
            background-color: #262730 !important;
            color: white !important;
        }
        div[data-baseweb="popover"] {
            background-color: #262730 !important;
            color: white !important;
        }
        div[data-baseweb="popover"] * {
            background-color: #262730 !important;
            color: white !important;
        }

        .export-button {
            text-align: right;
            margin-top: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# Title and instructions
st.title("💻 AI Code Generator")
st.markdown("### 🧠 Describe what you want and pick your language:")

# Language selector
languages = {
    "Python": "py", "JavaScript": "js", "Java": "java",
    "C++": "cpp", "C": "c", "C#": "cs", "HTML": "html",
    "CSS": "css", "TypeScript": "ts", "Go": "go",
    "Ruby": "rb", "PHP": "php"
}
language_name = st.selectbox("Select a programming language:", list(languages.keys()))
language_code = languages[language_name]

# User input prompt
user_prompt = st.text_area("Enter your code request:", placeholder=f"e.g. Create a login page using {language_name}")

# Function to generate code
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

# Generate and show code
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
        st.warning("Please enter a description for the code.")
