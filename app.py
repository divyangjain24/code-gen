import streamlit as st
import requests

# Set page config
st.set_page_config(page_title="AI Code Generator", layout="centered")

# Custom Glassmorphism CSS for beautiful UI
st.markdown("""
    <style>
        body {
            background: linear-gradient(to right, #141e30, #243b55);
        }

        .main {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 3rem;
            max-width: 800px;
            margin: auto;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        }

        h1 {
            text-align: center;
            color: #00d4ff;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }

        .stButton > button {
            background-color: #00d4ff;
            color: black;
            font-weight: bold;
            padding: 0.75rem 1.5rem;
            border: none;
            border-radius: 10px;
            transition: all 0.3s ease;
        }

        .stButton > button:hover {
            background-color: #009ec3;
            transform: scale(1.05);
        }

        /* Dropdown fix */
        div[data-baseweb="select"] {
            background-color: white !important;
            color: black !important;
            border-radius: 10px;
        }

        div[data-baseweb="select"] * {
            color: black !important;
        }

        .stSelectbox label {
            color: white !important;
            font-weight: bold;
        }

        .stTextArea label {
            color: white !important;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='main'>", unsafe_allow_html=True)
st.markdown("<h1>AI Code Generator 🤖💻</h1>", unsafe_allow_html=True)

# API Setup
OPENAI_API_KEY = st.secrets["OPENROUTER_API_KEY"]
OPENAI_ENDPOINT = "https://openrouter.ai/api/v1/chat/completions"

# Language selection
language = st.selectbox("Choose Programming Language", ["Python", "JavaScript", "Java", "C++", "Go"])

# Prompt input
user_prompt = st.text_area("🧠 Describe what your code should do:", placeholder="e.g., Make a calculator in selected language")

# Function to generate code
def generate_code(prompt, language):
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": f"You are a senior developer. Write clean, working code in {language} with proper comments."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.5,
        "max_tokens": 1000
    }

    try:
        response = requests.post(OPENAI_ENDPOINT, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        return f"❌ API Error: {e}"
    except Exception as e:
        return f"⚠️ Unexpected Error: {e}"

# Button and Output
if st.button("🚀 Generate Code"):
    if user_prompt.strip():
        st.markdown("### ✨ Generated Code:")
        code = generate_code(user_prompt, language)
        st.code(code, language=language.lower())
    else:
        st.warning("Please describe what kind of code you want.")

st.markdown("</div>", unsafe_allow_html=True)
