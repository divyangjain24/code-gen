import streamlit as st
import requests

# Load API Key
OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]
OPENROUTER_ENDPOINT = "https://openrouter.ai/api/v1/chat/completions"

# Page Configuration
st.set_page_config(page_title="AI Code Generator", layout="centered")

# Enhanced UI with Gradient and Glassmorphism
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');
        html, body {
            background: linear-gradient(135deg, #1e3c72, #2a5298);
            font-family: 'Inter', sans-serif;
            color: white;
        }
        .main {
            background: rgba(255, 255, 255, 0.08);
            backdrop-filter: blur(12px);
            padding: 3rem 2rem;
            border-radius: 25px;
            box-shadow: 0 12px 40px rgba(0, 0, 0, 0.3);
            max-width: 750px;
            margin: 3rem auto;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        h1 {
            text-align: center;
            color: #00f2fe;
            font-weight: 600;
            font-size: 2.5rem;
        }
        h3 {
            color: #ffffffcc;
        }
        .stButton > button {
            background-image: linear-gradient(to right, #00f2fe, #4facfe);
            color: white;
            border: none;
            padding: 0.75rem 1.5rem;
            font-size: 1rem;
            border-radius: 12px;
            font-weight: 600;
            transition: 0.3s ease-in-out;
            box-shadow: 0 4px 15px rgba(0, 242, 254, 0.3);
        }
        .stButton > button:hover {
            transform: scale(1.05);
            box-shadow: 0 6px 20px rgba(0, 242, 254, 0.5);
        }
        .stTextArea textarea {
            background-color: rgba(255, 255, 255, 0.05);
            color: white;
            border-radius: 10px;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        .stSelectbox div {
            background-color: rgba(255, 255, 255, 0.05);
            color: white;
        }
        .css-1y4p8pa {  /* Output Code box */
            background-color: #1f1f1f !important;
        }
    </style>
""", unsafe_allow_html=True)

# App Title and Description
st.markdown("<div class='main'><h1>💻 AI Code Generator 🤖</h1>", unsafe_allow_html=True)
st.markdown("### 🧠 Describe what code you want and choose a programming language:")

# Language Selector
languages = {
    "Python": "python",
    "JavaScript": "javascript",
    "Java": "java",
    "C++": "cpp",
    "C": "c",
    "C#": "csharp",
    "HTML": "html",
    "CSS": "css",
    "TypeScript": "typescript",
    "Go": "go",
    "Ruby": "ruby",
    "PHP": "php"
}
language_name = st.selectbox("Select a programming language:", list(languages.keys()))
language_code = languages[language_name]

# User Input Text Area
user_prompt = st.text_area(
    "Enter your code request:",
    placeholder=f"e.g. Create a weather app using {language_name}"
)

# Function to Generate Code using OpenRouter API
def generate_code(prompt, lang):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": f"You are a professional {lang} developer who writes clean, efficient, and well-commented code."},
            {"role": "user", "content": f"Generate an optimal and correct {lang} solution for the following task:\n{prompt}\nOnly provide the code without explanations."}
        ],
        "temperature": 0.5,
        "max_tokens": 1000
    }

    try:
        response = requests.post(OPENROUTER_ENDPOINT, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        if "choices" in result:
            return result["choices"][0]["message"]["content"]
        else:
            return "⚠️ No code returned from the model."
    except requests.exceptions.RequestException as e:
        return f"❌ API request failed: {str(e)}"
    except Exception as e:
        return f"⚠️ An error occurred: {str(e)}"

# Generate Button and Output Display
if st.button("✨ Generate Code"):
    if user_prompt.strip():
        with st.spinner("Generating your code..."):
            st.markdown(f"### 🚀 Code Output in {language_name}:")
            generated_code = generate_code(user_prompt, language_name)
            st.code(generated_code, language=language_code)
    else:
        st.warning("Please enter a description for the code.")

st.markdown("</div>", unsafe_allow_html=True)
